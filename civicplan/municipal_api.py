# SPDX-License-Identifier: AGPL-3.0-only
"""Staff-only municipal tracking. No public publication implied by a status."""

from fastapi import APIRouter, Depends, HTTPException, Query
from civicplan.source_api import repository, staff
from civicplan.workflow_api import call
from civicplan.municipal import MunicipalRepository, InitiativeInput, AmendmentInput

router = APIRouter(prefix="/api/v1/civicplan", tags=["Municipal tracking"])


def municipal(sources=Depends(repository)):
    return MunicipalRepository(sources)


@router.post("/initiatives", status_code=201)
def create_initiative(data: InitiativeInput, actor=Depends(staff), repo=Depends(municipal)):
    return call(repo.save, data, actor)


@router.post("/initiatives/{item_id}/revisions")
def update_initiative(
    item_id: str, data: InitiativeInput, actor=Depends(staff), repo=Depends(municipal)
):
    return call(repo.save, data, actor, item_id)


@router.post("/amendments", status_code=201)
def create_amendment(data: AmendmentInput, actor=Depends(staff), repo=Depends(municipal)):
    return call(repo.save, data, actor)


@router.post("/amendments/{item_id}/revisions")
def update_amendment(
    item_id: str, data: AmendmentInput, actor=Depends(staff), repo=Depends(municipal)
):
    return call(repo.save, data, actor, item_id)


@router.get("/municipal-work/{item_id}/history")
def history(item_id: str, actor=Depends(staff), repo=Depends(municipal)):
    rows = call(repo.history, item_id)
    if not rows:
        raise HTTPException(404, "Municipal workflow not found")
    return {"revisions": rows}


@router.get("/progress/targets")
def progress(
    policy_id: str | None = None,
    offset: int = Query(0, ge=0, le=100000),
    limit: int = Query(50, ge=1, le=100),
    actor=Depends(staff),
    repo=Depends(municipal),
):
    return call(repo.list, "initiative", policy_id=policy_id, offset=offset, limit=limit)


@router.get("/amendments/history")
def amendments(
    plan_type: str | None = None,
    offset: int = Query(0, ge=0, le=100000),
    limit: int = Query(50, ge=1, le=100),
    actor=Depends(staff),
    repo=Depends(municipal),
):
    return call(repo.list, "amendment", plan_type=plan_type, offset=offset, limit=limit)
