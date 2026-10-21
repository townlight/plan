"""P2 source-administration API behind the existing trusted staff-key boundary."""

import os
from typing import Annotated
from urllib.parse import quote

from civiccore.auth import staff_key_gate
from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import Response
from pydantic import Field
from sqlalchemy.exc import SQLAlchemyError

from civicplan.migrations import source_engine
from civicplan.source_bundle import BundleModel, PlanBundle
from civicplan.source_store import PlanSourceRepository, SourceConflict, SourcesUnavailable

router = APIRouter(prefix="/api/v1/civicplan", tags=["Planning source foundation"])
gate = staff_key_gate("CIVICPLAN_STAFF_API_KEY", "X-CivicPlan-Staff-Key")


def staff(
    role: Annotated[str | None, Header(alias="X-CivicPlan-Role")] = None,
    key: Annotated[str | None, Header(alias="X-CivicPlan-Staff-Key")] = None,
):
    gate(role=role, staff_key=key)
    # The shared key identifies a trusted service, not an individual person.
    return "trusted-staff-key"


def repository():
    url = os.environ.get("CIVICPLAN_POLICY_DB_URL")
    if not url:
        raise HTTPException(503, "Set CIVICPLAN_POLICY_DB_URL and run python -m civicplan.migrations.")
    engine = source_engine(url)
    try:
        yield PlanSourceRepository(engine)
    except SourcesUnavailable as exc:
        raise HTTPException(503, str(exc)) from None
    except SQLAlchemyError:
        raise HTTPException(503, "Planning source database unavailable; restore connectivity and retry.") from None
    finally:
        engine.dispose()


class ImportRequest(BundleModel):
    bundle: PlanBundle
    expected_previous_revision: str | None = Field(default=None, min_length=36, max_length=36)


@router.post("/source-imports")
def import_sources(
    request: ImportRequest, actor: str = Depends(staff), repo=Depends(repository),
):
    try:
        return repo.import_bundle(
            request.bundle, actor_id=actor, expected_previous_revision=request.expected_previous_revision,
        )
    except SourceConflict as exc:
        raise HTTPException(409, str(exc)) from None


@router.get("/source-plans/{plan_id}/history")
def source_history(plan_id: str, _actor=Depends(staff), repo=Depends(repository)):
    return {"revisions": repo.history(plan_id, staff=True), "audit": repo.audit(plan_id)}


@router.get("/source-revisions/{revision_id}")
def source_revision(revision_id: str, _actor=Depends(staff), repo=Depends(repository)):
    result = repo.revision(revision_id, staff=True)
    if result is None:
        raise HTTPException(404, "Planning source revision not found.")
    return result


@router.get("/source-revisions/{revision_id}/documents/{document_id}")
def source_document(revision_id: str, document_id: str, _actor=Depends(staff), repo=Depends(repository)):
    result = repo.original_document(revision_id, document_id, staff=True)
    if result is None:
        raise HTTPException(404, "Planning source document not found.")
    return Response(result["original_bytes"], media_type=result["media_type"], headers={
        "Content-Disposition": "attachment; filename*=UTF-8''" + quote(result["filename"], safe=""),
        "X-Content-SHA256": result["sha256"], "X-Content-Type-Options": "nosniff",
    })
