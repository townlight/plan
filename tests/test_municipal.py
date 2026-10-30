import copy
import os
from datetime import date

from fastapi.testclient import TestClient
import pytest
import sqlalchemy as sa
from civicplan.main import app
from civicplan.migrations import source_engine, upgrade
from civicplan.source_store import PlanSourceRepository
from civicplan.source_bundle import PlanBundle
from civicplan.municipal import MunicipalRepository
from source_fixtures import bundle

STAFF = {"X-CivicPlan-Role": "staff", "X-CivicPlan-Staff-Key": "municipal-fixture-key"}


@pytest.fixture
def context(tmp_path, monkeypatch):
    # A dedicated private PostgreSQL DB may be supplied by the acceptance harness.
    url = os.environ.get("PLANNING_MUNICIPAL_TEST_DB") or f"sqlite:///{tmp_path / 'municipal.db'}"
    engine = source_engine(url)
    upgrade(engine)
    sources = PlanSourceRepository(engine)
    initial = sources.import_bundle(
        PlanBundle.model_validate(bundle()), actor_id="fixture-importer"
    )
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", url)
    monkeypatch.setenv("CIVICPLAN_STAFF_API_KEY", STAFF["X-CivicPlan-Staff-Key"])
    monkeypatch.delenv("CIVICPLAN_DEMO_MODE", raising=False)
    ref = {
        "plan_id": "redstone-comprehensive",
        "revision_id": initial["revision_id"],
        "policy_id": "H-1",
    }
    with TestClient(app) as client:
        yield client, sources, ref
    engine.dispose()


def initiative(ref):
    return {
        "title": "Housing implementation",
        "policy": ref,
        "responsible_staff": "Fixture Planner",
        "target": "100",
        "unit": "homes",
        "due_on": "2027-12-31",
        "note": "Initial baseline",
    }


def test_progress_persists_with_history_and_conflict_refusal(context):
    client, sources, ref = context
    assert client.get("/api/v1/civicplan/progress/targets").status_code in (401, 403)
    data = initiative(ref)
    created = client.post("/api/v1/civicplan/initiatives", json=data, headers=STAFF)
    assert created.status_code == 201, created.text
    first = created.json()
    data.update(
        expected_revision=first["revision_id"],
        status="active",
        note="Measurement recorded",
        measurements=[
            {
                "recorded_on": date.today().isoformat(),
                "value": "15",
                "evidence": "Fixture measurement 1",
            }
        ],
    )
    endpoint = f"/api/v1/civicplan/initiatives/{first['item_id']}/revisions"
    updated = client.post(endpoint, json=data, headers=STAFF)
    assert updated.status_code == 200, updated.text
    assert client.post(endpoint, json=data, headers=STAFF).status_code == 409
    data["expected_revision"] = updated.json()["revision_id"]
    data["measurements"] = []
    assert client.post(endpoint, json=data, headers=STAFF).status_code == 422
    rows = MunicipalRepository(PlanSourceRepository(sources.engine)).history(first["item_id"])
    assert len(rows) == 2 and rows[-1]["snapshot"]["measurements"][0]["value"] == "15"
    assert rows[-1]["actor_id"] == "trusted-staff-key"
    response = client.get("/api/v1/civicplan/progress/targets?policy_id=H-1", headers=STAFF)
    assert response.status_code == 200 and response.json()["items"]
    assert (
        client.get("/api/v1/civicplan/progress/targets?policy_id=unknown", headers=STAFF).json()[
            "items"
        ]
        == []
    )
    with pytest.raises(sa.exc.DBAPIError), sources.engine.begin() as conn:
        conn.execute(
            sa.text("UPDATE civicplan.municipal_revisions SET sha256='bad'")
            if sources.engine.dialect.name == "postgresql"
            else sa.text("UPDATE municipal_revisions SET sha256='bad'")
        )


def test_amendment_requires_review_then_retained_adoption_source(context):
    client, sources, ref = context
    data = {
        "title": "Housing policy amendment",
        "policy": ref,
        "responsible_staff": "Fixture Planner",
        "proposal": "Proposed additional housing policy",
        "note": "Draft only",
    }
    created = client.post("/api/v1/civicplan/amendments", json=data, headers=STAFF)
    assert created.status_code == 201, created.text
    first = created.json()
    endpoint = f"/api/v1/civicplan/amendments/{first['item_id']}/revisions"
    data.update(
        expected_revision=first["revision_id"],
        status="adopted",
        review_note="Reviewed",
        adoption_revision=ref["revision_id"],
    )
    assert client.post(endpoint, json=data, headers=STAFF).status_code == 422
    data.update(status="review", adoption_revision=None, note="Ready for hearing")
    reviewed = client.post(endpoint, json=data, headers=STAFF)
    assert reviewed.status_code == 200, reviewed.text
    adopted = sources.import_bundle(
        PlanBundle.model_validate(bundle(change_note="Fictional amendment adopted")),
        actor_id="fixture-importer",
        expected_previous_revision=ref["revision_id"],
    )
    data.update(
        expected_revision=reviewed.json()["revision_id"],
        status="adopted",
        adoption_revision=adopted["revision_id"],
        note="Linked adopted source",
    )
    result = client.post(endpoint, json=data, headers=STAFF)
    assert result.status_code == 200, result.text
    assert result.json()["snapshot"]["adoption_source"]["bundle_sha256"] == adopted["bundle_sha256"]
    history = client.get(
        f"/api/v1/civicplan/municipal-work/{first['item_id']}/history", headers=STAFF
    )
    assert len(history.json()["revisions"]) == 3
    assert client.get("/api/v1/civicplan/amendments/history").status_code in (401, 403)
    data.update(
        expected_revision=result.json()["revision_id"], status="draft", adoption_revision=None
    )
    assert client.post(endpoint, json=data, headers=STAFF).status_code == 409


def test_creation_and_source_validation_refuse_shortcuts(context):
    client, _, ref = context
    data = initiative(ref)
    data["status"] = "completed"
    assert client.post("/api/v1/civicplan/initiatives", json=data, headers=STAFF).status_code == 422
    data = initiative(copy.deepcopy(ref))
    data["policy"]["plan_id"] = "another-plan"
    assert client.post("/api/v1/civicplan/initiatives", json=data, headers=STAFF).status_code == 422
