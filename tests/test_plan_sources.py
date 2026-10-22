import base64
from copy import deepcopy
from datetime import date
import hashlib
import os

from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest
import sqlalchemy as sa

from civicplan.main import app
from civicplan.migrations import ready, source_engine, upgrade
from civicplan.persistence import PlanPolicyRepository
from civicplan.source_bundle import PlanBundle
from civicplan.source_schema import documents, events, plans, revisions, policies, evidence
from civicplan.source_store import PlanSourceRepository, SourceConflict, SourcesUnavailable
from source_fixtures import bundle

STAFF = {"X-CivicPlan-Role": "staff", "X-CivicPlan-Staff-Key": "test-key"}


@pytest.mark.parametrize("document_id", ["folder/source", "folder\\source", "..", "source?download", "source#page"])
def test_import_rejects_document_ids_that_cannot_be_retrieved(document_id):
    data = bundle()
    data["documents"][0]["document_id"] = document_id
    data["policies"][0]["document_id"] = document_id
    data["adoption_evidence"][0]["document_id"] = document_id
    with pytest.raises(ValidationError, match="document_id"):
        PlanBundle.model_validate(data)


@pytest.fixture
def engine(tmp_path):
    result = source_engine(f"sqlite:///{tmp_path / 'sources.db'}")
    yield result
    result.dispose()


@pytest.fixture
def repo(engine):
    upgrade(engine)
    return PlanSourceRepository(engine)


def test_explicit_idempotent_migration_preserves_legacy_records(engine):
    legacy = PlanPolicyRepository(engine=engine, seed_defaults=True, initialize=True)
    record = legacy.create_staff_analysis(project_name="Legacy", proposal="housing near transit", policy_id="housing")
    with engine.connect() as connection:
        before = connection.execute(sa.text("SELECT * FROM plan_policy_records ORDER BY policy_id")).fetchall()
    assert not ready(engine)
    with pytest.raises(SourcesUnavailable):
        PlanSourceRepository(engine)
    upgrade(engine)
    upgrade(engine)
    assert ready(engine)
    with engine.connect() as connection:
        assert connection.execute(sa.text("SELECT * FROM plan_policy_records ORDER BY policy_id")).fetchall() == before
    reloaded = legacy.get_staff_analysis(record.analysis_id)
    assert reloaded.analysis_id == record.analysis_id
    assert reloaded.citations == record.citations
    assert reloaded.created_at.replace(tzinfo=record.created_at.tzinfo) == record.created_at
    assert PlanSourceRepository(engine).adopted_policies() == []


@pytest.mark.parametrize("plan_type", ["comprehensive", "small-area", "transportation", "parks", "sustainability"])
def test_all_plan_types_preserve_original_sources_and_structured_evidence(repo, plan_type):
    data = PlanBundle.model_validate(bundle(plan_type))
    first = repo.import_bundle(data, actor_id="test-staff")
    again = repo.import_bundle(data, actor_id="other-staff")
    assert first["created"] and not again["created"]
    assert first["revision_id"] == again["revision_id"]
    stored = repo.revision(first["revision_id"], staff=True)
    assert stored["adopted_on"] == date(2026, 2, 1)
    assert stored["source_date"] == date(2026, 1, 1)
    assert stored["status"] == "adopted"
    assert stored["policies"][0]["goal"] == "Housing choice"
    assert stored["adoption_evidence"][0]["kind"] == "manual-record"
    assert stored["adoption_evidence"][0]["reference"] == "Fictional adoption record 26-1"
    original = repo.original_document(first["revision_id"], "plan")
    assert original["original_bytes"] == data.documents[0].original_bytes()
    assert hashlib.sha256(original["original_bytes"]).hexdigest() == original["sha256"]
    assert repo.audit(data.plan_id)["ok"] and repo.audit(data.plan_id)["count"] == 1


def test_restart_corrections_pending_history_and_retirement(engine, repo):
    original = bundle()
    first = repo.import_bundle(PlanBundle.model_validate(original), actor_id="staff-a")
    pending = bundle(status="pending", change_note="Proposed amendment")
    second = repo.import_bundle(PlanBundle.model_validate(pending), actor_id="staff-b",
                                expected_previous_revision=first["revision_id"])
    assert repo.adopted_policies()[0]["revision_id"] == first["revision_id"]
    changed = deepcopy(original)
    text = "Fictional plan revised. Preserve more housing near services."
    changed["documents"][0]["content_base64"] = base64.b64encode(text.encode()).decode()
    changed["documents"][0]["sha256"] = hashlib.sha256(text.encode()).hexdigest()
    changed["policies"][0]["excerpt"] = "Preserve more housing near services."
    changed["change_note"] = "Human-recorded adopted amendment"
    changed["effective_on"] = "2026-04-01"
    third = repo.import_bundle(PlanBundle.model_validate(changed), actor_id="staff-c",
                               expected_previous_revision=second["revision_id"])
    engine.dispose()
    restarted = PlanSourceRepository(engine)
    assert restarted.revision(first["revision_id"], staff=True)["policies"][0]["excerpt"] == original["policies"][0]["excerpt"]
    assert restarted.adopted_policies(as_of=date(2026, 3, 15))[0]["revision_id"] == first["revision_id"]
    assert restarted.adopted_policies()[0]["revision_id"] == third["revision_id"]
    retired = bundle(status="superseded", change_note="Plan retired", effective_on="2026-05-01")
    restarted.import_bundle(PlanBundle.model_validate(retired), actor_id="staff-d",
                            expected_previous_revision=third["revision_id"])
    assert restarted.adopted_policies() == []
    assert len(restarted.history(original["plan_id"], staff=True)) == 4
    assert restarted.audit(original["plan_id"])["ok"]
    assert restarted.audit(original["plan_id"])["count"] == 4
    assert not restarted.import_bundle(PlanBundle.model_validate(original), actor_id="staff-a")["created"]
    assert restarted.adopted_policies() == []  # Reimporting old bytes does not reset the head.


def test_stale_revision_cannot_overwrite_and_import_is_atomic(repo, engine):
    data = PlanBundle.model_validate(bundle())
    first = repo.import_bundle(data, actor_id="staff-a")
    changed = bundle(change_note="Correction")
    with pytest.raises(SourceConflict):
        repo.import_bundle(PlanBundle.model_validate(changed), actor_id="staff-b")
    assert repo.history(data.plan_id, staff=True)[0]["revision_id"] == first["revision_id"]
    # Simulate storage failure halfway through a new import: everything must roll back.
    @sa.event.listens_for(engine, "before_cursor_execute")
    def fail_insert(_conn, _cursor, statement, _parameters, _context, _many):
        if statement.startswith("INSERT INTO main.source_policies"):
            raise RuntimeError("simulated storage failure")
    try:
        with pytest.raises(RuntimeError, match="simulated storage failure"):
            repo.import_bundle(PlanBundle.model_validate(bundle(plan_id="atomic-new")), actor_id="staff-a")
    finally:
        sa.event.remove(engine, "before_cursor_execute", fail_insert)
    assert repo.history("atomic-new", staff=True) == []
    with engine.connect() as connection:
        assert connection.execute(sa.select(plans).where(plans.c.plan_id == "atomic-new")).first() is None


@pytest.mark.parametrize("table", [revisions, documents, events, policies, evidence])
def test_database_rejects_mutation_of_historical_evidence(repo, engine, table):
    result = repo.import_bundle(PlanBundle.model_validate(bundle()), actor_id="staff")
    with pytest.raises(sa.exc.DatabaseError, match="append-only"):
        with engine.begin() as connection:
            connection.execute(table.delete().where(table.c.revision_id == result["revision_id"]))
    with pytest.raises(sa.exc.DatabaseError, match="append-only"):
        with engine.begin() as connection:
            column = {documents: "sha256", policies: "excerpt", evidence: "note"}.get(table, "actor_id")
            connection.execute(table.update().where(table.c.revision_id == result["revision_id"]).values(**{column: "tamper"}))


def test_private_pending_and_demo_sources_are_not_public_policies(repo):
    for key, changes in {
        "private": {"visibility": "staff"}, "pending": {"status": "pending"},
        "demo": {"dataset_kind": "demo"}, "future": {"effective_on": "2099-01-01"},
    }.items():
        result = repo.import_bundle(PlanBundle.model_validate(bundle(plan_id=key, **changes)), actor_id="staff")
        if key in {"private", "demo"}:
            assert repo.revision(result["revision_id"]) is None
            assert repo.original_document(result["revision_id"], "plan") is None
    assert repo.adopted_policies() == []


@pytest.mark.parametrize("mutate", [
    lambda d: d["documents"][0].update(sha256="0" * 64),
    lambda d: d["documents"][0].update(filename="../plan.txt"),
    lambda d: d["documents"][0].update(content_base64="invalid"),
    lambda d: d["policies"][0].update(document_id="missing"),
    lambda d: d["policies"][0].update(excerpt="Unsupported policy excerpt"),
    lambda d: d["policies"][0].update(staff_verified=False),
    lambda d: d.update(adoption_evidence=[]),
    lambda d: d.update(adopted_on=None),
    lambda d: d.update(documents=d["documents"] * 2),
    lambda d: d.update(policies=d["policies"] * 2),
    lambda d: d.update(plan_type="unrecognized"),
    lambda d: d.update(actor_id="spoofed"),
])
def test_invalid_bundles_fail_before_any_database_write(mutate):
    data = bundle()
    mutate(data)
    with pytest.raises(ValidationError):
        PlanBundle.model_validate(data)


def test_staff_api_import_history_download_and_public_boundary(engine, monkeypatch):
    upgrade(engine)
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", str(engine.url))
    monkeypatch.setenv("CIVICPLAN_STAFF_API_KEY", "test-key")
    client = TestClient(app)
    body = {"bundle": bundle()}
    assert client.post("/api/v1/civicplan/source-imports", json=body).status_code == 403
    wrong = {**STAFF, "X-CivicPlan-Staff-Key": "wrong"}
    assert client.post("/api/v1/civicplan/source-imports", json=body, headers=wrong).status_code == 403
    response = client.post("/api/v1/civicplan/source-imports", json=body, headers=STAFF)
    assert response.status_code == 200, response.text
    rid = response.json()["revision_id"]
    assert client.get(f"/api/v1/civicplan/source-revisions/{rid}").status_code == 403
    original = client.get(f"/api/v1/civicplan/source-revisions/{rid}/documents/plan", headers=STAFF)
    assert original.content == base64.b64decode(body["bundle"]["documents"][0]["content_base64"])
    assert original.headers["x-content-sha256"] == hashlib.sha256(original.content).hexdigest()
    history = client.get("/api/v1/civicplan/source-plans/redstone-comprehensive/history", headers=STAFF).json()
    assert history["audit"]["events"][0]["actor_id"] == "trusted-staff-key"
    assert history["audit"]["ok"]
    # The foundation's public lookup only sees adopted public policies, never sample fallback.
    found = client.post("/api/v1/civicplan/policies/lookup", json={"topic": "H-1"})
    assert found.status_code == 200 and found.json()["citation"] == "Fictional Plan, H-1"
    missing = client.post("/api/v1/civicplan/policies/lookup", json={"topic": "invented"})
    assert missing.status_code == 404
    no_answer = client.post("/api/v1/civicplan/questions/answer", json={"question": "xyz"}).json()
    assert no_answer["status"] == "no_supported_policy" and not no_answer["citations"]
    analysis = client.post("/api/v1/civicplan/staff-analysis/draft", json={
        "project_name": "Proposal", "proposal": "housing", "policy_id": "H-1",
    }, headers=STAFF)
    assert analysis.status_code == 200
    stored = client.get("/api/v1/civicplan/analyses/" + analysis.json()["analysis_id"], headers=STAFF).json()
    assert stored["payload"]["selected_policies"][0]["revision_id"] == rid
    second = {"bundle": bundle(plan_id="private", visibility="staff")}
    assert client.post("/api/v1/civicplan/source-imports", json=second, headers=STAFF).status_code == 200
    assert len(client.get("/api/v1/civicplan/plans/navigator").json()["plans"][0]["goals"][0]["objectives"][0]["policies"]) == 1


def test_api_requires_explicit_migration_and_does_not_seed(engine, monkeypatch):
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", str(engine.url))
    monkeypatch.setenv("CIVICPLAN_STAFF_API_KEY", "test-key")
    client = TestClient(app)
    response = client.post("/api/v1/civicplan/source-imports", json={"bundle": bundle()}, headers=STAFF)
    assert response.status_code == 503 and "migrations" in response.text
    assert not sa.inspect(engine).get_table_names()
    upgrade(engine)
    assert client.get("/api/v1/civicplan/plans/navigator").json()["plans"] == []
    assert PlanPolicyRepository(engine=engine).list_policies() == ()


def test_postgresql_sources_migrations_restart_and_immutability():
    url = os.environ.get("PLANNING_TEST_DATABASE_URL")
    if not url:
        if os.environ.get("CI"):
            pytest.fail("CI must supply the isolated Planning PostgreSQL test database.")
        pytest.skip("Set PLANNING_TEST_DATABASE_URL for PostgreSQL acceptance.")
    engine = source_engine(url)
    assert engine.dialect.name == "postgresql"
    try:
        legacy = PlanPolicyRepository(engine=engine, seed_defaults=True, initialize=True)
        legacy_record = legacy.create_staff_analysis(
            project_name="Legacy PostgreSQL acceptance", proposal="housing near transit", policy_id="housing",
        )
        with engine.connect() as connection:
            before = connection.execute(sa.text(
                "SELECT * FROM civicplan.plan_policy_records ORDER BY policy_id"
            )).fetchall()
        upgrade(engine)
        upgrade(engine)
        with engine.connect() as connection:
            assert connection.execute(sa.text(
                "SELECT * FROM civicplan.plan_policy_records ORDER BY policy_id"
            )).fetchall() == before
        assert legacy.get_staff_analysis(legacy_record.analysis_id) == legacy_record
        repository = PlanSourceRepository(engine)
        from uuid import uuid4
        prefix = str(uuid4())
        for kind in ["comprehensive", "small-area", "transportation", "parks", "sustainability"]:
            data = PlanBundle.model_validate(bundle(kind, plan_id=prefix + kind))
            imported = repository.import_bundle(data, actor_id="pg-acceptance")
            assert repository.audit(data.plan_id)["ok"]
            with pytest.raises(sa.exc.DatabaseError, match="append-only"):
                with engine.begin() as connection:
                    connection.execute(revisions.delete().where(revisions.c.revision_id == imported["revision_id"]))
            engine.dispose()
            repository = PlanSourceRepository(engine)
            assert repository.original_document(imported["revision_id"], "plan")["original_bytes"] == data.documents[0].original_bytes()
    finally:
        engine.dispose()


def test_integrity_detects_corrupted_source_after_storage_guard_bypass(repo, engine):
    result = repo.import_bundle(PlanBundle.model_validate(bundle()), actor_id="staff")
    assert repo.verify_sources("redstone-comprehensive")["ok"]
    # Simulate corrupted recovery media in this isolated test database.
    with engine.begin() as connection:
        connection.execute(sa.text("DROP TRIGGER source_documents_update"))
        connection.execute(documents.update().where(documents.c.revision_id == result["revision_id"]).values(
            original_bytes=b"corrupted source",
        ))
    assert not repo.verify_sources("redstone-comprehensive")["ok"]
    assert not repo.audit("redstone-comprehensive")["ok"]


def test_default_unconfigured_app_never_loads_samples(monkeypatch):
    monkeypatch.delenv("CIVICPLAN_POLICY_DB_URL", raising=False)
    monkeypatch.delenv("CIVICPLAN_DEMO_MODE", raising=False)
    client = TestClient(app)
    for response in (client.get("/api/v1/civicplan/plans/navigator"),
                     client.post("/api/v1/civicplan/questions/answer", json={"question": "housing"})):
        assert response.status_code == 503 and "CIVICPLAN_POLICY_DB_URL" in response.text
        assert "Comprehensive Plan, Housing Element" not in response.text
    assert client.post("/api/v1/civicplan/export", json={"title": "real", "policy_id": "housing"}).status_code == 403


def test_database_failure_is_actionable_without_secret_or_sample(monkeypatch):
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", "postgresql+psycopg2://not-a-user:secret-never-returned@127.0.0.1:1/missing?connect_timeout=1")
    response = TestClient(app).get("/api/v1/civicplan/plans/navigator")
    assert response.status_code == 503
    assert "secret-never-returned" not in response.text
    assert "retry" in response.text
    assert "Comprehensive Plan, Housing Element" not in response.text
