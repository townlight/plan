import pytest
from fastapi.testclient import TestClient

from civicplan.consistency import check_policy_consistency
from civicplan.main import app
from civicplan.policy_lookup import lookup_plan_policy
from civicplan.records_export import build_policy_export
from civicplan.staff_analysis import draft_staff_analysis


client = TestClient(app)


def test_policy_lookup_returns_cited_plan_policy() -> None:
    result = lookup_plan_policy(topic="missing middle housing near transit")

    assert result.policy_id == "comp-plan-housing-2.1"
    assert result.citation == "Comprehensive Plan, Housing Element, Policy H-2.1"
    assert "missing-middle housing" in result.excerpt
    assert "does not make land-use determinations" in result.disclaimer


def test_policy_consistency_keeps_planner_review_boundary() -> None:
    result = check_policy_consistency(
        proposal="Mixed-use housing near transit, sidewalks, and a neighborhood park.",
        policy_id="comp-plan-housing-2.1",
    )

    assert result.status == "potentially-consistent"
    assert len(result.factors) >= 2
    assert "planner of record" in result.staff_next_step.casefold()
    assert "does not make" in result.disclaimer


def test_staff_analysis_draft_is_cited_and_review_required() -> None:
    result = draft_staff_analysis(
        project_name="Maple Avenue Homes",
        proposal="A duplex project near a school and transit stop.",
        policy_id="housing",
    )

    assert result.heading == "Plan consistency context for Maple Avenue Homes"
    assert "Comprehensive Plan, Housing Element, Policy H-2.1" in result.citations
    assert result.review_required is True
    assert any("Planner of record" in bullet for bullet in result.bullets)


def test_policy_export_preserves_records_context() -> None:
    result = build_policy_export(title="Maple Avenue Plan Context", policy_id="housing")

    assert result.title == "Maple Avenue Plan Context"
    assert result.policy_id == "housing"
    assert "Preserve source plan citation and excerpt." in result.checklist
    assert "municipal planning record" in result.retention_note


def test_policy_lookup_api_success_shape() -> None:
    response = client.post(
        "/api/v1/civicplan/policies/lookup",
        json={"topic": "transportation safety near school", "plan_type": "transportation"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["policy_id"] == "transportation-plan-3.4"
    assert payload["citation"].startswith("Transportation Plan")
    assert payload["disclaimer"]


def test_zoning_policy_context_api_returns_cited_review_required_contract() -> None:
    response = client.post(
        "/api/v1/civicplan/context/zoning",
        json={
            "topic": "missing middle housing near transit",
            "zone_code": "R-2",
            "use": "ADU",
            "civiczone_context_id": "zone-question-123",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["policy_id"] == "comp-plan-housing-2.1"
    assert payload["plan_type"] == "comprehensive"
    assert payload["citation"] == "Comprehensive Plan, Housing Element, Policy H-2.1"
    assert payload["excerpt"]
    assert payload["relevance"]
    assert payload["review_required"] is True
    assert payload["source"] == "sample"
    assert payload["civiczone_context_id"] == "zone-question-123"
    assert "not a zoning determination" in payload["boundary"]
    assert "legal advice" in payload["boundary"]
    assert "does not make land-use determinations" in payload["disclaimer"]


def test_zoning_policy_context_validation_is_actionable() -> None:
    response = client.post("/api/v1/civicplan/context/zoning", json={})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert "topic" in detail["message"]
    assert "non-empty topic" in detail["fix"]
    assert "topic" in detail["fields"]


def test_existing_endpoint_validation_remains_endpoint_neutral() -> None:
    response = client.post("/api/v1/civicplan/consistency/check", json={})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert "policy_id" in detail["fields"]
    assert "proposal" in detail["fields"]
    assert "zone_code" not in detail["fix"]
    assert "fields array" in detail["fix"]


def test_oversized_policy_lookup_validation_is_actionable() -> None:
    response = client.post(
        "/api/v1/civicplan/policies/lookup",
        json={"topic": "x" * 501, "plan_type": "comprehensive"},
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert "topic" in detail["fields"]
    assert "fields array" in detail["fix"]


def test_consistency_and_staff_analysis_apis() -> None:
    consistency = client.post(
        "/api/v1/civicplan/consistency/check",
        json={"proposal": "Housing near transit and sidewalks.", "policy_id": "housing"},
    )
    staff = client.post(
        "/api/v1/civicplan/staff-analysis/draft",
        json={
            "project_name": "Maple Avenue Homes",
            "proposal": "Housing near transit and sidewalks.",
            "policy_id": "housing",
        },
    )

    assert consistency.status_code == 200
    assert consistency.json()["status"] == "potentially-consistent"
    assert staff.status_code == 200
    assert staff.json()["review_required"] is True


def test_public_ui_route_is_accessible_and_honest() -> None:
    response = client.get("/civicplan")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    text = response.text
    assert '<a class="skip-link" href="#main">Skip to main content</a>' in text
    assert '<main id="main" tabindex="-1">' in text
    assert "0.3.0+dev.1 explicit static sample" in text
    assert "<button" not in text
    assert "<textarea" not in text
    assert "Static sample proposal" in text
    assert "Plan navigator" in text
    assert "Progress tracking" in text
    assert "does not make zoning" in text
    assert "official planning determinations" in text
    assert "certified ADA" not in text


@pytest.fixture(autouse=True)
def explicit_sample_mode(monkeypatch):
    monkeypatch.setenv("CIVICPLAN_DEMO_MODE", "1")
