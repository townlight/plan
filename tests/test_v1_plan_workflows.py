import pytest
from fastapi.testclient import TestClient

import civicplan.main as main_module
from civicplan.integration_mocks import CivicPlanIntegrationMockLayer, IntegrationError
from civicplan.main import app


client = TestClient(app)
STAFF_HEADERS = {"X-CivicPlan-Role": "staff", "X-CivicPlan-Staff-Key": "test-staff-key"}


@pytest.fixture(autouse=True)
def reset_policy_repository() -> None:
    main_module._dispose_policy_repository()


def test_plan_navigator_groups_policy_structure() -> None:
    response = client.get("/api/v1/civicplan/plans/navigator")

    assert response.status_code == 200
    payload = response.json()
    assert payload["plans"][0]["plan_type"] == "comprehensive"
    assert payload["plans"][0]["policies"][0]["citation"]
    assert "staff verify applicability" in payload["boundary"]


def test_plan_question_answer_and_synthesis_are_cited_and_review_required() -> None:
    answer = client.post(
        "/api/v1/civicplan/questions/answer",
        json={"question": "What does the plan say about missing middle housing?"},
    )
    synthesis = client.post(
        "/api/v1/civicplan/plans/synthesis",
        json={"topic": "housing affordability near parks and services"},
    )

    assert answer.status_code == 200
    assert answer.json()["status"] == "answered"
    assert answer.json()["review_required"] is True
    assert answer.json()["citations"]
    assert synthesis.status_code == 200
    assert synthesis.json()["review_required"] is True
    assert synthesis.json()["citations"]


def test_amendment_history_distinguishes_pending_from_adopted() -> None:
    response = client.get("/api/v1/civicplan/amendments/history")

    assert response.status_code == 200
    statuses = {item["adoption_status"] for item in response.json()["items"]}
    assert {"adopted", "pending"} <= statuses
    assert "Pending amendments are not treated as adopted" in response.json()["boundary"]


def test_progress_targets_return_evidence_and_boundary() -> None:
    response = client.get("/api/v1/civicplan/progress/targets?policy_id=parks-plan-1.2")

    assert response.status_code == 200
    payload = response.json()
    assert payload["items"][0]["policy_id"] == "parks-plan-1.2"
    assert payload["items"][0]["evidence"]
    assert "not official findings" in payload["boundary"]


def test_civicclerk_context_is_draft_only_and_cited() -> None:
    response = client.post(
        "/api/v1/civicplan/context/civicclerk",
        json={"agenda_item": "North corridor rezoning staff report", "topic": "housing"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["review_required"] is True
    assert payload["citations"]
    assert "draft-only" in payload["boundary"]


def test_staff_policy_ingestion_requires_complete_sources(tmp_path, monkeypatch) -> None:
    from civicplan.migrations import source_engine, upgrade
    from source_fixtures import bundle
    monkeypatch.setenv("CIVICPLAN_STAFF_API_KEY", "test-staff-key")
    old = client.post("/api/v1/civicplan/policies/ingest", json=_ingest_payload(), headers=STAFF_HEADERS)
    assert old.status_code == 409 and "source-imports" in old.text
    engine = source_engine(f"sqlite:///{tmp_path / 'policies.db'}")
    upgrade(engine)
    engine.dispose()
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", str(engine.url))
    created = client.post("/api/v1/civicplan/source-imports", json={"bundle": bundle()}, headers=STAFF_HEADERS)
    assert created.status_code == 200
    found = client.post("/api/v1/civicplan/policies/lookup", json={"topic": "H-1"})
    assert found.status_code == 200 and found.json()["citation"] == "Fictional Plan, H-1"


def test_policy_ingestion_preserves_pending_status(tmp_path, monkeypatch) -> None:
    from civicplan.migrations import source_engine, upgrade
    from source_fixtures import bundle
    engine = source_engine(f"sqlite:///{tmp_path / 'pending.db'}")
    upgrade(engine)
    engine.dispose()
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", str(engine.url))
    monkeypatch.setenv("CIVICPLAN_STAFF_API_KEY", "test-staff-key")
    created = client.post("/api/v1/civicplan/source-imports",
                          json={"bundle": bundle(status="pending")}, headers=STAFF_HEADERS)
    assert created.status_code == 200
    rid = created.json()["revision_id"]
    stored = client.get(f"/api/v1/civicplan/source-revisions/{rid}", headers=STAFF_HEADERS).json()
    assert stored["status"] == "pending" and stored["adoption_evidence"]
    assert client.get("/api/v1/civicplan/plans/navigator").json()["plans"] == []


def test_integration_mocks_reject_live_endpoints_and_malformed_payloads() -> None:
    layer = CivicPlanIntegrationMockLayer()
    live = layer.run("geojson_area_boundary", {"url": "https://example.test/geojson"})
    malformed = layer.run("local_plan_document_import", {"policies": []})
    ok = layer.run(
        "civicclerk_staff_report_context",
        {"agenda_item": "Housing hearing", "staff_report_id": "sr-1"},
    )

    assert isinstance(live, IntegrationError)
    assert live.code == "air_gap_violation"
    assert isinstance(malformed, IntegrationError)
    assert malformed.code == "malformed_payload"
    assert not isinstance(ok, IntegrationError)
    assert ok.records[0]["visibility"] == "staff_only"


def _ingest_payload() -> dict[str, str]:
    return {
        "topic_key": "resilience",
        "policy_id": "sustainability-plan-4.2",
        "plan_type": "sustainability",
        "title": "Heat resilience corridors",
        "citation": "Sustainability Plan, Climate Chapter, Policy C-4.2",
        "excerpt": "Prioritize shade, cool pavement, and emergency cooling access in heat-vulnerable corridors.",
        "relevance": "Relevant for street redesign, park investment, and capital planning.",
        "adoption_status": "adopted",
        "source_document": "2025 Sustainability Plan",
    }


@pytest.fixture(autouse=True)
def explicit_sample_mode(monkeypatch):
    monkeypatch.setenv("CIVICPLAN_DEMO_MODE", "1")
