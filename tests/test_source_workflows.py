import hashlib
import json
import os
from datetime import date
from uuid import uuid4

from fastapi.testclient import TestClient
import pytest
import sqlalchemy as sa

from civicplan.main import app
from civicplan.migrations import source_engine, upgrade
from civicplan.policy_service import PolicyService
from civicplan.source_bundle import PlanBundle
from civicplan.source_store import PlanSourceRepository, SourceConflict
from civicplan.workflow_models import AnalysisInput
from civicplan.workflow_store import WorkflowRepository
from civicplan.connections import ConnectionUnavailable
from civicplan.workflow_schema import versions, snapshots, events
from source_fixtures import bundle

STAFF = {'X-CivicPlan-Role': 'staff', 'X-CivicPlan-Staff-Key': 'workflow-key'}


@pytest.fixture
def context(tmp_path, monkeypatch):
    url = f'sqlite:///{tmp_path / "workflows.db"}'
    engine = source_engine(url)
    upgrade(engine)
    sources = PlanSourceRepository(engine)
    imported = sources.import_bundle(PlanBundle.model_validate(bundle()), actor_id='import-staff')
    ref = {'plan_id': 'redstone-comprehensive', 'revision_id': imported['revision_id'], 'policy_id': 'H-1'}
    monkeypatch.setenv('CIVICPLAN_POLICY_DB_URL', url)
    monkeypatch.setenv('CIVICPLAN_STAFF_API_KEY', 'workflow-key')
    client = TestClient(app)
    yield sources, WorkflowRepository(sources), ref, client
    engine.dispose()


def draft(ref, **changes):
    data = {'project_name': 'Fictional source-backed review', 'proposal': 'CONFIDENTIAL staff proposal',
            'selected_policies': [ref], 'staff_notes': 'PRIVATE internal note'}
    data.update(changes)
    return AnalysisInput.model_validate(data)


def reviewed(ref, **changes):
    data = {'audience': 'public', 'review_state': 'reviewed', 'reviewer_label': 'Recorded staff reviewer',
            'reviewed_on': date.today().isoformat(), 'review_notes': 'Sources and applicability reviewed by staff.',
            'analysis_text': 'Staff-edited policy analysis with conditional applicability.',
            'public_summary': 'Staff-selected public explanation with cited policy context.'}
    data.update(changes)
    return draft(ref, **data)


def test_staff_inventories_page_current_heads_without_private_text(context):
    sources, workflow, ref, _ = context
    sources.import_bundle(PlanBundle.model_validate(bundle(plan_id='private-plan', visibility='staff')), actor_id='a')
    page = sources.inventory(limit=1)
    assert len(page['items']) == 1 and page['next_offset'] == 1
    assert len(sources.inventory(limit=1, offset=1)['items']) == 1
    assert sources.inventory(offset=2)['items'] == []
    first = workflow.save(draft(ref), 'account-a')
    second = workflow.save(reviewed(ref, expected_previous_revision=first['revision_id']), 'account-b', first['analysis_id'])
    item = workflow.inventory()['items'][0]
    assert item['revision_id'] == second['revision_id']
    assert item['review_state'] == 'reviewed'
    assert 'PRIVATE' not in json.dumps(item) and 'CONFIDENTIAL' not in json.dumps(item)
    with sources.engine.connect() as conn:
        actors = conn.execute(sa.select(versions.c.actor_id).order_by(versions.c.created_at)).scalars().all()
    assert actors == ['account-a', 'account-b']
    history = workflow.history_page(first['analysis_id'], limit=1)
    assert history['next_offset'] == 1
    assert history['items'][0]['actor_id'] == 'account-a'
    assert 'PRIVATE' not in json.dumps(history) and 'CONFIDENTIAL' not in json.dumps(history)
    assert workflow.history_page(first['analysis_id'], limit=1, offset=1)['items'][0]['actor_id'] == 'account-b'
    sources.import_bundle(PlanBundle.model_validate(bundle(change_note='Historical amendment')),
                          actor_id='b', expected_previous_revision=ref['revision_id'])
    history = sources.history_page(ref['plan_id'], limit=1)
    assert history['next_offset'] == 1 and history['items'][0]['revision_id'] == ref['revision_id']
    assert sources.history_page(ref['plan_id'], limit=1, offset=1)['next_offset'] is None
    for invalid in ({'limit': 0}, {'limit': 101}, {'offset': -1}, {'offset': 100001}):
        with pytest.raises(ValueError):
            sources.inventory(**invalid)
        with pytest.raises(ValueError):
            workflow.inventory(**invalid)
        with pytest.raises(ValueError):
            workflow.snapshot_inventory(**invalid)
        with pytest.raises(ValueError):
            workflow.history_page(first['analysis_id'], **invalid)
        with pytest.raises(ValueError):
            sources.history_page(ref['plan_id'], **invalid)


def test_snapshot_preview_is_write_free_exact_and_permission_rechecked(context):
    sources, workflow, ref, _ = context
    saved = workflow.save(reviewed(ref), 'account-a')
    preview = workflow.preview_snapshot(saved['analysis_id'], saved['revision_id'], 'public')
    assert workflow.audit(saved['analysis_id'])['count'] == 1
    assert workflow.snapshot_inventory(staff=True)['items'] == []
    snapshot = workflow.snapshot(saved['analysis_id'], saved['revision_id'], 'public', 'account-a')
    assert snapshot['text'] == preview['text'] and snapshot['sha256'] == preview['sha256']
    workflow.snapshot(saved['analysis_id'], saved['revision_id'], 'staff_only', 'account-a')
    assert len(workflow.snapshot_inventory()['items']) == 1
    assert len(workflow.snapshot_inventory(staff=True)['items']) == 2
    workflow.save(draft(ref, expected_previous_revision=saved['revision_id']), 'account-b', saved['analysis_id'])
    with pytest.raises(SourceConflict):
        workflow.preview_snapshot(saved['analysis_id'], saved['revision_id'], 'public')
    private = bundle(visibility='staff', change_note='Public permission revoked')
    sources.import_bundle(PlanBundle.model_validate(private), actor_id='account-b', expected_previous_revision=ref['revision_id'])
    assert workflow.snapshot_inventory()['items'] == []


def test_all_consumers_use_imported_version_and_never_general_sample(context):
    sources, workflow, ref, client = context
    for endpoint, payload in (
        ('policies/lookup', {'topic': 'housing'}),
        ('questions/answer', {'question': 'housing'}),
        ('plans/synthesis', {'topic': 'housing'}),
        ('consistency/check', {'proposal': 'housing', 'policy_id': 'H-1'}),
        ('context/zoning', {'topic': 'housing'}),
        ('context/civicclerk', {'topic': 'housing', 'agenda_item': 'Fictional hearing'}),
    ):
        response = client.post('/api/v1/civicplan/' + endpoint, json=payload)
        assert response.status_code == 200, response.text
        assert ref['revision_id'] in response.text
        assert 'Fictional Plan, H-1' in response.text
        assert 'H-2.1' not in response.text
    navigation = client.get('/api/v1/civicplan/plans/navigator').json()
    policy = navigation['plans'][0]['goals'][0]['objectives'][0]['policies'][0]
    assert policy['source_sha256'] == bundle()['documents'][0]['sha256']
    assert client.get(policy['source_location']).content == PlanBundle.model_validate(bundle()).documents[0].original_bytes()
    answer = PolicyService(sources).answer('Who is the mayor?')
    assert answer['status'] == 'no_supported_policy' and not answer['citations']
    saved = workflow.save(draft(ref), 'staff-key')
    assert workflow.get(saved['analysis_id'])['payload']['policy_context'][0]['revision_id'] == ref['revision_id']


def test_conflicting_sources_are_a_review_task_and_private_policies_require_auth(context):
    sources, workflow, ref, client = context
    second = bundle('small-area', plan_id='different-plan')
    second['policies'][0]['excerpt'] = 'Fictional Redstone Valley plan.'
    sources.import_bundle(PlanBundle.model_validate(second), actor_id='staff')
    result = client.post('/api/v1/civicplan/policies/search', json={'query': 'housing'}).json()
    assert result['status'] == 'needs_review' and len(result['review_task']['source_references']) == 2
    private = bundle(plan_id='private-plan', visibility='staff')
    private['policies'][0]['policy_id'] = 'PRIVATE-ID'
    sources.import_bundle(PlanBundle.model_validate(private), actor_id='staff')
    assert 'PRIVATE-ID' not in client.get('/api/v1/civicplan/plans/navigator').text
    assert 'PRIVATE-ID' in client.get('/api/v1/civicplan/plans/navigator', headers=STAFF).text
    assert client.get('/api/v1/civicplan/plans/navigator', headers={**STAFF, 'X-CivicPlan-Staff-Key': 'bad'}).status_code == 403


def test_analysis_revisions_review_and_immutable_exports_survive_amendment(context):
    sources, workflow, ref, client = context
    first = workflow.save(draft(ref), 'service')
    with pytest.raises(ValueError, match='review'):
        workflow.snapshot(first['analysis_id'], first['revision_id'], 'public', 'service')
    new = workflow.save(reviewed(ref, expected_previous_revision=first['revision_id'], considerations=[
        {'policy': ref, 'stance': 'conflicting', 'note': 'Staff identify a proposal-specific conflict.'}]), 'service', first['analysis_id'])
    public = workflow.snapshot(first['analysis_id'], new['revision_id'], 'public', 'service')
    assert 'CONFIDENTIAL' not in public['text'] and 'PRIVATE' not in public['text']
    assert 'Staff-selected public explanation' in public['text']
    assert json.loads(public['text'])['policy_sources'][0]['revision_id'] == ref['revision_id']
    assert public['sha256'] == hashlib.sha256(public['text'].encode()).hexdigest()
    revision = bundle(change_note='Later adopted amendment')
    revision['policies'][0]['citation'] = 'Fictional amended policy citation'
    sources.import_bundle(PlanBundle.model_validate(revision), actor_id='staff', expected_previous_revision=ref['revision_id'])
    assert workflow.public_documents(source_id=public['source_id'])[0] == public
    found = client.post('/api/v1/civicplan/questions/answer', json={'question': 'housing'}).json()
    assert found['sources'][0]['revision_id'] != ref['revision_id']
    assert found['citations'] == ['Fictional amended policy citation']
    assert workflow.get(first['analysis_id'], first['revision_id'])['payload']['review_state'] == 'draft'
    sources.engine.dispose()
    restarted = WorkflowRepository(PlanSourceRepository(sources.engine))
    assert restarted.document(public['version']) == public
    assert restarted.audit(first['analysis_id'])['ok']
    with pytest.raises(SourceConflict):
        workflow.save(draft(ref, expected_previous_revision=first['revision_id'], analysis_text='stale edit'), 'service', first['analysis_id'])
    with pytest.raises(ValueError, match='public'):
        private = workflow.save(reviewed(ref, audience='staff'), 'service')
        workflow.snapshot(private['analysis_id'], private['revision_id'], 'public', 'service')


@pytest.mark.parametrize('table', [versions, snapshots, events])
def test_workflow_history_is_immutable(context, table):
    sources, workflow, ref, client = context
    saved = workflow.save(reviewed(ref), 'staff')
    workflow.snapshot(saved['analysis_id'], saved['revision_id'], 'public', 'staff')
    with pytest.raises(sa.exc.DatabaseError, match='append-only'):
        with sources.engine.begin() as conn:
            conn.execute(table.delete())
    assert workflow.audit(saved['analysis_id'])['ok']


def test_api_review_export_and_authorization(context):
    sources, workflow, ref, client = context
    data = reviewed(ref).model_dump(mode='json')
    assert client.post('/api/v1/civicplan/analyses', json=data).status_code == 403
    assert client.post('/api/v1/civicplan/analyses', json={**data, 'actor_id': 'spoof'}, headers=STAFF).status_code == 422
    saved = client.post('/api/v1/civicplan/analyses', json=data, headers=STAFF).json()
    path = '/api/v1/civicplan/analyses/' + saved['analysis_id']
    assert client.get(path).status_code == 403
    snapshot = client.post(path + '/snapshots', json={'expected_revision': saved['revision_id'], 'visibility': 'public'}, headers=STAFF)
    assert snapshot.status_code == 200, snapshot.text
    sid = snapshot.json()['version']
    exported = client.get('/api/v1/civicplan/snapshots/' + sid + '/export', headers=STAFF)
    assert exported.status_code == 200
    assert exported.headers['x-content-sha256'] == hashlib.sha256(exported.content).hexdigest()
    assert exported.json()['policy_sources'][0]['revision_id'] == ref['revision_id']
    assert client.get(path + '/history', headers=STAFF).json()['audit']['ok']


def test_connected_sources_recheck_permissions_and_never_return_cached_text(context):
    sources, workflow, ref, client = context
    text = 'Explicitly public fictional meeting adoption record'
    doc = {'source_id': 'townlight:meetings:archive:fixture:minutes', 'title': 'Fictional meeting',
           'text': text, 'sha256': hashlib.sha256(text.encode()).hexdigest(), 'version': 'fixture',
           'visibility': 'public', 'citation': 'Fictional approved minutes'}
    state = [doc]
    workflow.providers = {'meetings': lambda **kwargs: state}
    link = {'provider': 'meetings', 'relation': 'adoption-evidence', 'source_id': doc['source_id'], 'expected_sha256': doc['sha256']}
    saved = workflow.save(reviewed(ref, linked_sources=[link]), 'staff')
    snapshot = workflow.snapshot(saved['analysis_id'], saved['revision_id'], 'public', 'staff')
    assert text in snapshot['text']
    state[:] = [{**doc, 'visibility': 'staff_only'}]
    assert workflow.public_documents() == []
    with pytest.raises(ConnectionUnavailable):
        workflow.get(saved['analysis_id'])
    with pytest.raises(ConnectionUnavailable):
        workflow.document(snapshot['version'], staff=True)
    assert workflow.audit(saved['analysis_id'])['ok']
    state[:] = [doc]
    assert workflow.document(snapshot['version']) == snapshot


def test_future_sources_and_later_private_revision_do_not_grant_public_access(context):
    sources, workflow, ref, client = context
    saved = workflow.save(reviewed(ref), 'staff')
    snapshot = workflow.snapshot(saved['analysis_id'], saved['revision_id'], 'public', 'staff')
    future = bundle(change_note='Future adoption', effective_on='2099-01-01')
    imported = sources.import_bundle(PlanBundle.model_validate(future), actor_id='staff',
                                     expected_previous_revision=ref['revision_id'])
    assert client.get('/api/v1/civicplan/policy-sources/' + imported['revision_id'] + '/documents/plan').status_code == 404
    assert workflow.public_documents(source_id=snapshot['source_id']) == [snapshot]
    private = bundle(change_note='Staff-only current revision', visibility='staff')
    sources.import_bundle(PlanBundle.model_validate(private), actor_id='staff',
                          expected_previous_revision=imported['revision_id'])
    assert workflow.public_documents(source_id=snapshot['source_id']) == []
    assert client.get('/api/v1/civicplan/policy-sources/' + ref['revision_id'] + '/documents/plan').status_code == 404
    assert workflow.get(saved['analysis_id']) is not None
    assert workflow.audit(saved['analysis_id'])['ok']


def test_postgresql_workflow_storage_and_mutation_guards():
    url = os.environ.get('PLANNING_TEST_DATABASE_URL')
    if not url:
        if os.environ.get('CI'):
            pytest.fail('PostgreSQL workflow acceptance requires PLANNING_TEST_DATABASE_URL.')
        pytest.skip('Set PLANNING_TEST_DATABASE_URL for PostgreSQL workflow acceptance.')
    engine = source_engine(url)
    try:
        upgrade(engine)
        sources = PlanSourceRepository(engine)
        plan_id = 'workflow-pg-' + str(uuid4())
        imported = sources.import_bundle(PlanBundle.model_validate(bundle(plan_id=plan_id)), actor_id='fixture-staff')
        ref = {'plan_id': plan_id, 'revision_id': imported['revision_id'], 'policy_id': 'H-1'}
        workflow = WorkflowRepository(sources)
        saved = workflow.save(reviewed(ref), 'fixture-staff')
        snapshot = workflow.snapshot(saved['analysis_id'], saved['revision_id'], 'public', 'fixture-staff')
        for table in (versions, snapshots, events):
            with pytest.raises(sa.exc.DatabaseError, match='append-only'):
                with engine.begin() as conn:
                    conn.execute(table.delete().where(table.c.analysis_id == saved['analysis_id']))
        engine.dispose()
        reconnected = WorkflowRepository(PlanSourceRepository(engine))
        assert reconnected.document(snapshot['version']) == snapshot
        assert reconnected.audit(saved['analysis_id'])['ok']
    finally:
        engine.dispose()
