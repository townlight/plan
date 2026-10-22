"""Source-backed workflow API; staff service auth and trusted provider injection."""
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import Response
from pydantic import Field
from urllib.parse import quote

from civicplan.connections import ConnectionUnavailable, search
from civicplan.source_api import repository, staff, gate
from civicplan.source_bundle import BundleModel
from civicplan.source_store import SourceConflict
from civicplan.policy_service import PolicyService
from civicplan.workflow_models import AnalysisInput
from civicplan.workflow_store import WorkflowRepository

router = APIRouter(prefix='/api/v1/civicplan', tags=['Planning source workflows'])


def workflows(request: Request, sources=Depends(repository)):
    return WorkflowRepository(sources, getattr(request.app.state, 'planning_providers', {}),
                              getattr(request.app.state, 'planning_access_rewrite', None))


def audience(role: Annotated[str | None, Header(alias='X-CivicPlan-Role')] = None,
             key: Annotated[str | None, Header(alias='X-CivicPlan-Staff-Key')] = None):
    if role is not None or key is not None:
        gate(role=role, staff_key=key)
        return True
    return False


def call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except SourceConflict as exc:
        raise HTTPException(409, str(exc)) from None
    except ConnectionUnavailable as exc:
        raise HTTPException(503, str(exc)) from None
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from None


@router.post('/analyses')
def create_analysis(data: AnalysisInput, actor=Depends(staff), repo=Depends(workflows)):
    if data.expected_previous_revision is not None:
        raise HTTPException(422, 'New analyses have no previous revision.')
    return call(repo.save, data, actor)


@router.post('/analyses/{analysis_id}/revisions')
def revise_analysis(analysis_id: str, data: AnalysisInput, actor=Depends(staff), repo=Depends(workflows)):
    if data.expected_previous_revision is None:
        raise HTTPException(422, 'Supply the analysis previous revision.')
    return call(repo.save, data, actor, analysis_id)


@router.get('/analyses/{analysis_id}')
def read_analysis(analysis_id: str, revision_id: str | None = None, actor=Depends(staff), repo=Depends(workflows)):
    result = call(repo.get, analysis_id, revision_id)
    if result is None:
        raise HTTPException(404, 'Analysis not found.')
    return result


@router.get('/analyses/{analysis_id}/history')
def analysis_history(analysis_id: str, actor=Depends(staff), repo=Depends(workflows)):
    return {'revisions': call(repo.history, analysis_id), 'audit': call(repo.audit, analysis_id)}


class SnapshotInput(BundleModel):
    expected_revision: str = Field(min_length=36, max_length=36)
    visibility: Literal['staff_only', 'public'] = 'staff_only'


@router.post('/analyses/{analysis_id}/snapshots')
def create_snapshot(analysis_id: str, data: SnapshotInput, actor=Depends(staff), repo=Depends(workflows)):
    return call(repo.snapshot, analysis_id, data.expected_revision, data.visibility, actor)


@router.get('/snapshots/{snapshot_id}')
def read_snapshot(snapshot_id: str, actor=Depends(staff), repo=Depends(workflows)):
    result = call(repo.document, snapshot_id, staff=True)
    if result is None:
        raise HTTPException(404, 'Snapshot not found.')
    return result


@router.get('/snapshots/{snapshot_id}/export')
def export_snapshot(snapshot_id: str, actor=Depends(staff), repo=Depends(workflows)):
    result = read_snapshot(snapshot_id, actor, repo)
    return Response(result['text'], media_type='application/json', headers={
        'Content-Disposition': f'attachment; filename="planning-{snapshot_id}.json"',
        'X-Content-SHA256': result['sha256'], 'X-Content-Type-Options': 'nosniff'})


@router.post('/snapshots/{snapshot_id}/access-advice')
def access_advice(snapshot_id: str, actor=Depends(staff), repo=Depends(workflows)):
    return call(repo.access_advice, snapshot_id)


class SearchInput(BundleModel):
    query: str = Field(min_length=1, max_length=2000)
    plan_type: str | None = Field(default=None, max_length=40)


@router.post('/policies/search')
def search_policies(data: SearchInput, is_staff=Depends(audience), sources=Depends(repository)):
    return call(PolicyService(sources).answer, data.query, staff=is_staff, plan_type=data.plan_type)


class ConnectionSearch(BundleModel):
    provider: Literal['meetings', 'zoning']
    query: str = Field(min_length=1, max_length=500)


@router.post('/connections/search')
def search_connections(data: ConnectionSearch, actor=Depends(staff), repo=Depends(workflows)):
    return call(search, repo.providers, data.provider, data.query)


@router.get('/policy-sources/{revision_id}/documents/{document_id}')
def public_original(revision_id: str, document_id: str, sources=Depends(repository)):
    if not PolicyService(sources).public_permitted(revision_id):
        raise HTTPException(404, 'Public policy source unavailable.')
    document = sources.original_document(revision_id, document_id)
    if document is None:
        raise HTTPException(404, 'Public policy document not found.')
    return Response(document['original_bytes'], media_type=document['media_type'], headers={
        'Content-Disposition': "attachment; filename*=UTF-8''" + quote(document['filename'], safe=''),
        'X-Content-SHA256': document['sha256'], 'X-Content-Type-Options': 'nosniff'})
