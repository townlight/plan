"""Public plan exploration over persisted sources (task-owned acceptance).

These tests exercise the *public* surface the beta promises: exploring stored,
adopted, effective, public plan revisions by topic/goal/plan type/keyword, with
citations, and a public/staff revision boundary that cannot be bypassed by naming
an id. Synthetic fictional plan data only.

Every bundle here satisfies the source-integrity rule that an excerpt must occur
in its own referenced document, because that rule is what makes a citation real.
"""
import base64
import hashlib
import os

from fastapi.testclient import TestClient
import pytest
from civicplan.main import app
from civicplan.migrations import source_engine, upgrade
from civicplan.source_store import PlanSourceRepository
from civicplan.source_bundle import PlanBundle
from civicplan.policy_service import PolicyService

STAFF = {"X-CivicPlan-Role": "staff", "X-CivicPlan-Staff-Key": "public-explore-key"}


def document(*paragraphs):
    """One fictional source document; returns (document, sha256 hex)."""
    text = '\n\n'.join(paragraphs) + '\n'
    raw = text.encode()
    return {'document_id': 'plan', 'filename': 'plan.txt', 'media_type': 'text/plain',
            'sha256': hashlib.sha256(raw).hexdigest(),
            'content_base64': base64.b64encode(raw).decode()}


def base_bundle():
    excerpt = 'Preserve housing choice near civic services.'
    doc = document('Fictional Redstone Valley plan.', excerpt)
    return {'plan_id': 'redstone-comprehensive', 'title': 'Fictional Redstone Valley Plan',
            'jurisdiction': 'Fictional Redstone Valley', 'plan_type': 'comprehensive',
            'status': 'adopted', 'visibility': 'public', 'source_date': '2026-01-01',
            'adopted_on': '2026-02-01', 'effective_on': '2026-03-01',
            'change_note': 'Initial test adoption', 'reviewer_label': 'Fictional Planner',
            'documents': [doc], 'policies': [{
                'policy_id': 'H-1', 'document_id': 'plan', 'goal': 'Housing choice',
                'objective': 'Access to services', 'topic_key': 'housing',
                'neighborhoods': ['Northbank'],
                'title': 'Housing policy', 'citation': 'Fictional Plan, H-1',
                'anchor': 'paragraph 1', 'excerpt': excerpt,
                'relevance': 'Staff confirm applicability.', 'staff_verified': True}],
            'adoption_evidence': [{'kind': 'manual-record',
                                   'reference': 'Fictional adoption record 26-1',
                                   'document_id': 'plan',
                                   'note': 'Test-only staff-recorded adoption.'}]}


@pytest.fixture
def context(tmp_path, monkeypatch):
    url = os.environ.get("PLANNING_PUBLIC_TEST_DB") or f"sqlite:///{tmp_path / 'public.db'}"
    engine = source_engine(url)
    upgrade(engine)
    sources = PlanSourceRepository(engine)
    initial = sources.import_bundle(PlanBundle.model_validate(base_bundle()),
                                    actor_id="fixture-importer")

    # A staff-only plan. Public readers must never see it, even when the same
    # wording would otherwise match.
    staff_excerpt = 'Staff-only working note about housing choice.'
    staff = base_bundle()
    staff.update(plan_id='redstone-internal', title='Fictional Internal Working Plan',
                 visibility='staff', documents=[document('Fictional internal working plan.',
                                                         staff_excerpt)],
                 policies=[{**staff['policies'][0], 'policy_id': 'S-9',
                            'goal': 'Internal working goal', 'topic_key': 'internal',
                            'citation': 'Fictional Internal Plan, S-9',
                            'excerpt': staff_excerpt}])
    sources.import_bundle(PlanBundle.model_validate(staff), actor_id="fixture-importer")

    # A pending amendment of the public plan: not adopted, so not public yet.
    pending_excerpt = 'Pending housing amendment text.'
    pending = base_bundle()
    pending.update(status='pending', change_note='Pending amendment under review',
                   documents=[document('Fictional Redstone Valley plan.',
                                       'Pending housing amendment text.')],
                   policies=[{**pending['policies'][0], 'policy_id': 'H-2',
                              'excerpt': pending_excerpt}])
    # A second revision of the SAME plan must name the revision it supersedes;
    # the store refuses a silent second head.
    pending_revision = sources.import_bundle(PlanBundle.model_validate(pending),
                                             actor_id="fixture-importer",
                                             expected_previous_revision=initial["revision_id"])

    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", url)
    monkeypatch.setenv("CIVICPLAN_STAFF_API_KEY", STAFF["X-CivicPlan-Staff-Key"])
    monkeypatch.delenv("CIVICPLAN_DEMO_MODE", raising=False)
    ref = {"plan_id": "redstone-comprehensive", "revision_id": initial["revision_id"],
           "policy_id": "H-1", "pending_revision_id": pending_revision["revision_id"]}
    with TestClient(app) as client:
        yield client, sources, ref
    engine.dispose()


def test_public_exploration_reads_persisted_adopted_public_plan(context):
    client, _sources, ref = context
    api = client.get("/api/v1/civicplan/public/plan-explore")
    assert api.status_code == 200, api.text
    payload = api.json()
    assert payload["total"] == 1, payload
    plan = payload["plans"][0]
    assert plan["plan_id"] == ref["plan_id"]
    assert plan["revision_id"] == ref["revision_id"]
    policy = plan["goals"][0]["objectives"][0]["policies"][0]
    assert policy["citation"] == "Fictional Plan, H-1"
    assert policy["anchor"] == "paragraph 1"
    assert policy["filename"] == "plan.txt"
    assert len(policy["source_sha256"]) == 64
    assert policy["source_location"].startswith("/api/v1/civicplan/policy-sources/")
    assert "Preserve housing choice" in policy["excerpt"]
    assert payload["review_required"] is True
    assert payload["disclaimer"]
    assert payload["facets"]["topics"] == ["housing"]
    assert payload["facets"]["plans"][0]["plan_id"] == ref["plan_id"]


def test_public_exploration_page_is_rendered_from_the_same_persisted_data(context):
    client, _sources, ref = context
    page = client.get("/civicplan")
    assert page.status_code == 200, page.text
    body = page.text
    assert "Fictional Redstone Valley Plan" in body
    assert "Fictional Plan, H-1" in body
    assert ref["revision_id"] in body
    for sample in ("0.3.0+dev.1 explicit static sample", "Housing proposal context",
                   "A small mixed-use housing project near transit"):
        assert sample not in body, sample
    assert 'name="q"' in body and 'action="/civicplan"' in body
    assert 'method="get"' in body


def test_exploration_filters_match_persisted_dimensions(context):
    client, _sources, ref = context
    assert client.get("/api/v1/civicplan/public/plan-explore",
                      params={"q": "housing"}).json()["total"] == 1
    assert client.get("/api/v1/civicplan/public/plan-explore",
                      params={"goal": "Housing choice"}).json()["total"] == 1
    assert client.get("/api/v1/civicplan/public/plan-explore",
                      params={"topic": "housing"}).json()["total"] == 1
    assert client.get("/api/v1/civicplan/public/plan-explore",
                      params={"plan_type": "comprehensive"}).json()["total"] == 1
    empty = client.get("/api/v1/civicplan/public/plan-explore",
                       params={"q": "heliport"}).json()
    assert empty["total"] == 0 and empty["plans"] == []
    assert empty["empty_reason"]
    empty_page = client.get("/civicplan", params={"q": "heliport"})
    assert empty_page.status_code == 200
    assert "Nothing to show" in empty_page.text and "heliport" in empty_page.text


def test_public_exploration_never_exposes_staff_only_or_pending_revisions(context):
    client, _sources, ref = context
    payload = client.get("/api/v1/civicplan/public/plan-explore").json()
    plan_ids = {plan["plan_id"] for plan in payload["plans"]}
    assert "redstone-internal" not in plan_ids
    revision_ids = {plan["revision_id"] for plan in payload["plans"]}
    assert ref["pending_revision_id"] not in revision_ids
    page = client.get("/civicplan").text
    assert "Internal working goal" not in page
    assert "Pending housing amendment text" not in page
    denied = client.get(f"/api/v1/civicplan/public/policy/{ref['revision_id']}/S-9")
    assert denied.status_code == 404, denied.text
    pending = client.get(
        f"/api/v1/civicplan/public/policy/{ref['pending_revision_id']}/H-2")
    assert pending.status_code == 404, pending.text


def test_public_citation_endpoint_returns_the_cited_stored_policy(context):
    client, _sources, ref = context
    response = client.get(
        f"/api/v1/civicplan/public/policy/{ref['revision_id']}/{ref['policy_id']}")
    assert response.status_code == 200, response.text
    policy = response.json()
    assert policy["citation"] == "Fictional Plan, H-1"
    assert policy["revision_id"] == ref["revision_id"]
    assert policy["review_required"] is True
    assert policy["relevance"] == "Staff confirm applicability."


def test_staff_audience_still_sees_staff_revisions_and_public_does_not(context):
    client, sources, ref = context
    staff_view = PolicyService(sources).navigator(staff=True)
    assert any(plan["plan_id"] == "redstone-internal" for plan in staff_view["plans"])
    public_view = client.get("/api/v1/civicplan/public/plan-explore").json()
    assert all(plan["plan_id"] != "redstone-internal" for plan in public_view["plans"])


def test_page_says_unavailable_instead_of_showing_sample_text(tmp_path, monkeypatch):
    monkeypatch.delenv("CIVICPLAN_POLICY_DB_URL", raising=False)
    monkeypatch.delenv("CIVICPLAN_DEMO_MODE", raising=False)
    with TestClient(app) as client:
        page = client.get("/civicplan")
        assert page.status_code == 200
        assert "not available" in page.text.lower()
        assert "Housing proposal context" not in page.text
        api = client.get("/api/v1/civicplan/public/plan-explore")
        assert api.status_code == 503


def test_neighborhood_navigation_uses_imported_applicability_not_keywords(context):
    client, sources, _ = context
    south = base_bundle()
    south['plan_id'] = 'southbank-plan'
    south['policies'][0]['neighborhoods'] = ['Southbank']
    # Both plans have identical text and topic; the imported applicability differs.
    sources.import_bundle(PlanBundle.model_validate(south), actor_id='fixture-importer')
    for name, expected in [('Northbank', 'redstone-comprehensive'), ('Southbank', 'southbank-plan')]:
        result = client.get('/api/v1/civicplan/public/plan-explore', params={
            'neighborhood': name, 'goal': 'Housing choice', 'topic': 'housing'}).json()
        assert result['total'] == 1
        assert result['plans'][0]['plan_id'] == expected
        policy = result['plans'][0]['goals'][0]['objectives'][0]['policies'][0]
        assert name in policy['neighborhoods']
        assert client.get(policy['source_location']).status_code == 200
        assert sources.verify_sources(expected)['ok']
    page = client.get('/civicplan', params={'neighborhood': 'Southbank'}).text
    assert 'name="neighborhood"' in page and 'value="Southbank" selected' in page
    missing = client.get('/api/v1/civicplan/public/plan-explore', params={'neighborhood': 'Unknown'}).json()
    assert missing['total'] == 0
    assert 'Unknown' in missing['empty_reason']
