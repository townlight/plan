from fastapi.testclient import TestClient

import townlight_planning.main as main_module
from townlight_planning.main import app
from townlight_planning.persistence import PlanPolicyRepository


client = TestClient(app)


def test_policy_and_staff_analysis_records_persist(tmp_path) -> None:
    db_path = tmp_path / "policy-records.db"
    repository = PlanPolicyRepository(db_url=f"sqlite:///{db_path}", seed_defaults=True, initialize=True)

    policy = repository.lookup_policy(topic="housing", plan_type="comprehensive")
    stored = repository.create_staff_analysis(
        project_name="Maple Avenue Homes",
        proposal="Housing near transit and sidewalks.",
        policy_id="housing",
    )
    repository.engine.dispose()

    second_repository = PlanPolicyRepository(db_url=f"sqlite:///{db_path}", seed_defaults=False)
    try:
        reloaded_policy = second_repository.lookup_policy(topic="housing")
        reloaded_analysis = second_repository.get_staff_analysis(stored.analysis_id)
    finally:
        second_repository.engine.dispose()

    assert reloaded_policy == policy
    assert reloaded_analysis is not None
    assert reloaded_analysis.heading == "Plan consistency context for Maple Avenue Homes"
    assert "Comprehensive Plan, Housing Element, Policy H-2.1" in reloaded_analysis.citations
    db_path.unlink(missing_ok=True)


def test_municipal_staff_analysis_does_not_use_sample_policy(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("TOWNLIGHT_PLANNING_POLICY_DB_URL", f"sqlite:///{tmp_path / 'municipal.db'}")
    monkeypatch.setenv("TOWNLIGHT_PLANNING_STAFF_API_KEY", "test-staff-key")
    response = client.post("/api/v1/townlight_planning/staff-analysis/draft", json={
        "project_name": "Actual proposal", "proposal": "Housing near services", "policy_id": "real-policy",
    }, headers={"X-Townlight-Planning-Role": "staff", "X-Townlight-Planning-Staff-Key": "test-staff-key"})
    assert response.status_code == 503
    assert "migrations" in response.text


def test_persisted_staff_analysis_requires_staff_role(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "staff-auth.db"
    monkeypatch.setenv("TOWNLIGHT_PLANNING_POLICY_DB_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("TOWNLIGHT_PLANNING_STAFF_API_KEY", "test-staff-key")

    try:
        create_response = client.post(
            "/api/v1/townlight_planning/staff-analysis/draft",
            json={
                "project_name": "Maple Avenue Homes",
                "proposal": "CONFIDENTIAL: acquire parcel 123 before public notice.",
                "policy_id": "housing",
            },
        )
        get_response = client.get("/api/v1/townlight_planning/staff-analysis/not-authorized")
    finally:
        main_module._dispose_policy_repository()
        main_module._policy_db_url = None

    assert create_response.status_code == 403
    assert get_response.status_code == 403
    assert "X-Townlight-Planning-Role: staff" in create_response.json()["detail"]["fix"]
    db_path.unlink(missing_ok=True)


def test_staff_analysis_rejects_oversized_persisted_proposal(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "staff-validation.db"
    monkeypatch.setenv("TOWNLIGHT_PLANNING_POLICY_DB_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("TOWNLIGHT_PLANNING_STAFF_API_KEY", "test-staff-key")

    try:
        response = client.post(
            "/api/v1/townlight_planning/staff-analysis/draft",
            json={
                "project_name": "Maple Avenue Homes",
                "proposal": "x" * 5001,
                "policy_id": "housing",
            },
            headers={"X-Townlight-Planning-Role": "staff", "X-Townlight-Planning-Staff-Key": "test-staff-key"},
        )
    finally:
        main_module._dispose_policy_repository()
        main_module._policy_db_url = None

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert "proposal" in detail["fields"]
    assert "fields array" in detail["fix"]
    db_path.unlink(missing_ok=True)


def test_zoning_context_does_not_substitute_sample_for_municipal_data(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("TOWNLIGHT_PLANNING_POLICY_DB_URL", f"sqlite:///{tmp_path / 'municipal.db'}")
    response = client.post("/api/v1/townlight_planning/context/zoning", json={"topic": "accessory dwelling unit"})
    assert response.status_code == 503
    assert "migrations" in response.text


def test_staff_analysis_lookup_requires_configured_database() -> None:
    response = client.get("/api/v1/townlight_planning/staff-analysis/not-configured")

    assert response.status_code == 503
    assert "Set TOWNLIGHT_PLANNING_POLICY_DB_URL" in response.json()["detail"]["fix"]
