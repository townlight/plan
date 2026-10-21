"""FastAPI runtime foundation for Townlight Planning."""

import os
from typing import Annotated

from civiccore import __version__ as CIVICCORE_VERSION
from civiccore.auth import staff_key_gate
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from civicplan import __version__
from civicplan.consistency import check_policy_consistency
from civicplan.integration_mocks import CivicPlanIntegrationMockLayer, IntegrationError
from civicplan.plan_workflows import (
    amendment_history,
    answer_plan_question,
    civicclerk_staff_report_context,
    normalize_ingested_policy,
    plan_navigator,
    progress_targets,
    synthesize_plan_context,
)
from civicplan.persistence import PlanPolicyRepository, StoredStaffAnalysis
from civicplan.policy_lookup import PlanPolicy
from civicplan.policy_lookup import lookup_plan_policy
from civicplan.public_ui import render_public_lookup_page
from civicplan.records_export import build_policy_export
from civicplan.staff_analysis import draft_staff_analysis


app = FastAPI(
    title='Townlight Planning',
    version=__version__,
    description='Comprehensive-plan policy lookup and cited planning analysis support for Townlight.',
)

_policy_repository: PlanPolicyRepository | None = None
_policy_db_url: str | None = None
_require_staff_key = staff_key_gate("CIVICPLAN_STAFF_API_KEY", "X-CivicPlan-Staff-Key")


class PolicyLookupRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)
    plan_type: str = Field(default="comprehensive", min_length=1, max_length=120)


class ZoningPolicyContextRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)
    zone_code: str | None = Field(default=None, max_length=80)
    use: str | None = Field(default=None, max_length=160)
    parcel_number: str | None = Field(default=None, max_length=120)
    address: str | None = Field(default=None, max_length=500)
    plan_type: str = Field(default="comprehensive", min_length=1, max_length=120)
    civiczone_context_id: str | None = Field(default=None, max_length=160)


class ConsistencyRequest(BaseModel):
    proposal: str = Field(min_length=1, max_length=5000)
    policy_id: str = Field(min_length=1, max_length=160)


class StaffAnalysisRequest(BaseModel):
    project_name: str = Field(min_length=1, max_length=500)
    proposal: str = Field(min_length=1, max_length=5000)
    policy_id: str = Field(min_length=1, max_length=160)


class PolicyExportRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    policy_id: str = Field(min_length=1, max_length=160)
    format: str = Field(default="markdown", min_length=1, max_length=40)


class PolicyIngestRequest(BaseModel):
    topic_key: str = Field(min_length=1, max_length=160)
    policy_id: str = Field(min_length=1, max_length=160)
    plan_type: str = Field(min_length=1, max_length=120)
    title: str = Field(min_length=1, max_length=500)
    citation: str = Field(min_length=1, max_length=500)
    excerpt: str = Field(min_length=1, max_length=5000)
    relevance: str = Field(min_length=1, max_length=2000)
    adoption_status: str = Field(default="adopted", min_length=1, max_length=80)
    source_document: str = Field(min_length=1, max_length=500)


class PlanQuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    plan_type: str = Field(default="comprehensive", min_length=1, max_length=120)


class PlanSynthesisRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)


class CivicClerkContextRequest(BaseModel):
    agenda_item: str = Field(min_length=1, max_length=500)
    topic: str = Field(min_length=1, max_length=500)


class IntegrationMockRequest(BaseModel):
    provider: str = Field(min_length=1, max_length=120)
    payload: dict[str, object] = Field(default_factory=dict)


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicPlan",
        "version": __version__,
        "status": "v1 cited planning policy and staff analysis runtime",
        "message": (
            "Townlight Planning v0.2.2 provides cited plan-policy lookup, staff-only local policy ingestion, "
            "goal/objective/policy navigation, cited plan Q&A, cross-plan synthesis, amendment history, progress tracking, "
            "Townlight Zoning and Townlight Meetings context contracts, optional database-backed policy and staff-analysis records, records-ready exports, "
            "local adversarial integration mocks, and an accessible public UI. It does not make official planning determinations, "
            "provide legal advice, call live external systems by default, or replace planner/elected-body judgment."
        ),
        "next_step": "Configure local plan policies with CIVICPLAN_POLICY_DB_URL and keep official actions in staff review.",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "civicplan",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    fields = sorted(
        {
            ".".join(str(part) for part in error.get("loc", [])[1:])
            for error in exc.errors()
            if len(error.get("loc", [])) > 1
        }
    )
    field_list = ", ".join(fields) if fields else "request body"
    if request.url.path == "/api/v1/civicplan/context/zoning":
        fix = (
            "Send a JSON body with a non-empty topic and optional zone_code, use, "
            "parcel_number, address, plan_type, and civiczone_context_id fields."
        )
    else:
        fix = (
            "Send a JSON body that includes the required field names listed in "
            "the fields array, using strings for text inputs."
        )
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "message": f"Townlight Planning could not validate: {field_list}.",
                "fix": fix,
                "fields": fields,
            }
        },
    )


@app.get("/civicplan", response_class=HTMLResponse)
def public_civicplan_page() -> str:
    """Return the public sample plan-policy lookup UI."""

    return render_public_lookup_page()


@app.post("/api/v1/civicplan/policies/lookup")
def policy_lookup(request: PolicyLookupRequest) -> dict[str, object]:
    result = _lookup_plan_policy(topic=request.topic, plan_type=request.plan_type)
    return result.__dict__


@app.post("/api/v1/civicplan/policies/ingest")
def ingest_policy(
    request: PolicyIngestRequest,
    x_civicplan_role: Annotated[str | None, Header()] = None,
    x_civicplan_staff_key: Annotated[str | None, Header()] = None,
) -> dict[str, object]:
    if _policy_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Townlight Planning policy ingestion requires configured local persistence.",
                "fix": "Set CIVICPLAN_POLICY_DB_URL, then retry the staff-only ingestion request.",
            },
        )
    _require_staff_role(x_civicplan_role, x_civicplan_staff_key)
    try:
        record = normalize_ingested_policy(**request.model_dump())
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={"message": "Plan policy ingestion payload is invalid.", "fix": str(exc)},
        ) from exc
    policy = _get_policy_repository().upsert_policy(
        topic_key=record.topic_key,
        policy=record.policy,
    )
    return {
        "policy": policy.__dict__,
        "adoption_status": record.adoption_status,
        "source_document": record.source_document,
        "review_required": True,
    }


@app.get("/api/v1/civicplan/plans/navigator")
def plans_navigator(plan_type: str | None = None) -> dict[str, object]:
    policies = _list_plan_policies(plan_type=plan_type)
    return plan_navigator(policies)


@app.post("/api/v1/civicplan/questions/answer")
def plan_question_answer(request: PlanQuestionRequest) -> dict[str, object]:
    policies = _list_plan_policies(plan_type=request.plan_type)
    result = answer_plan_question(
        question=request.question,
        plan_type=request.plan_type,
        policies=policies,
    )
    return result.__dict__


@app.post("/api/v1/civicplan/plans/synthesis")
def plan_synthesis(request: PlanSynthesisRequest) -> dict[str, object]:
    return synthesize_plan_context(topic=request.topic, policies=_list_plan_policies())


@app.get("/api/v1/civicplan/amendments/history")
def plan_amendment_history(plan_type: str | None = None) -> dict[str, object]:
    return {
        "items": [amendment.__dict__ for amendment in amendment_history(plan_type=plan_type)],
        "boundary": "Pending amendments are not treated as adopted plan text.",
    }


@app.get("/api/v1/civicplan/progress/targets")
def plan_progress_targets(policy_id: str | None = None) -> dict[str, object]:
    return {
        "items": [
            {
                **target.__dict__,
                "updated_at": target.updated_at.isoformat(),
            }
            for target in progress_targets(policy_id=policy_id)
        ],
        "boundary": "Progress statuses are planning-support evidence, not official findings.",
    }


@app.post("/api/v1/civicplan/context/civicclerk")
def civicclerk_context(request: CivicClerkContextRequest) -> dict[str, object]:
    return civicclerk_staff_report_context(
        agenda_item=request.agenda_item,
        topic=request.topic,
    )


@app.post("/api/v1/civicplan/integrations/mock")
def integration_mock(request: IntegrationMockRequest) -> dict[str, object]:
    result = CivicPlanIntegrationMockLayer().run(request.provider, request.payload)
    if isinstance(result, IntegrationError):
        raise HTTPException(
            status_code=422,
            detail={
                "message": result.message,
                "fix": result.fix,
                "code": result.code,
                "provider": result.provider,
            },
        )
    return {
        "provider": result.provider,
        "records": list(result.records),
        "source": result.source,
        "warnings": list(result.warnings),
    }


@app.post("/api/v1/civicplan/context/zoning")
def zoning_policy_context(request: ZoningPolicyContextRequest) -> dict[str, object]:
    policy, source = _lookup_plan_policy_with_source(
        topic=_zoning_context_topic(request),
        plan_type=request.plan_type,
    )
    return {
        "policy_id": policy.policy_id,
        "plan_type": policy.plan_type,
        "citation": policy.citation,
        "excerpt": policy.excerpt,
        "relevance": policy.relevance,
        "disclaimer": policy.disclaimer,
        "review_required": True,
        "source": source,
        "civiczone_context_id": request.civiczone_context_id,
        "boundary": (
            "Townlight Planning provides cited comprehensive-plan context only; it is not a "
            "zoning determination, planning approval, or legal advice."
        ),
    }


@app.post("/api/v1/civicplan/consistency/check")
def consistency_check(request: ConsistencyRequest) -> dict[str, object]:
    result = check_policy_consistency(proposal=request.proposal, policy_id=request.policy_id)
    return result.__dict__


@app.post("/api/v1/civicplan/staff-analysis/draft")
def staff_analysis(
    request: StaffAnalysisRequest,
    x_civicplan_role: Annotated[str | None, Header()] = None,
    x_civicplan_staff_key: Annotated[str | None, Header()] = None,
) -> dict[str, object]:
    if _policy_database_url() is not None:
        _require_staff_role(x_civicplan_role, x_civicplan_staff_key)
        stored = _get_policy_repository().create_staff_analysis(
            project_name=request.project_name,
            proposal=request.proposal,
            policy_id=request.policy_id,
        )
        return _stored_staff_analysis_response(stored)

    result = draft_staff_analysis(
        project_name=request.project_name,
        proposal=request.proposal,
        policy_id=request.policy_id,
    )
    payload = result.__dict__
    payload["analysis_id"] = None
    return payload


@app.get("/api/v1/civicplan/staff-analysis/{analysis_id}")
def get_staff_analysis(
    analysis_id: str,
    x_civicplan_role: Annotated[str | None, Header()] = None,
    x_civicplan_staff_key: Annotated[str | None, Header()] = None,
) -> dict[str, object]:
    if _policy_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Townlight Planning policy persistence is not configured.",
                "fix": "Set CIVICPLAN_POLICY_DB_URL to retrieve persisted staff-analysis records.",
            },
        )
    _require_staff_role(x_civicplan_role, x_civicplan_staff_key)
    stored = _get_policy_repository().get_staff_analysis(analysis_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Staff-analysis record not found.",
                "fix": "Use an analysis_id returned by POST /api/v1/civicplan/staff-analysis/draft.",
            },
        )
    return _stored_staff_analysis_response(stored)


@app.post("/api/v1/civicplan/export")
def policy_export(request: PolicyExportRequest) -> dict[str, object]:
    result = build_policy_export(title=request.title, policy_id=request.policy_id, format=request.format)
    return result.__dict__


def _policy_database_url() -> str | None:
    return os.environ.get("CIVICPLAN_POLICY_DB_URL")


def _get_policy_repository() -> PlanPolicyRepository:
    global _policy_db_url, _policy_repository
    db_url = _policy_database_url()
    if db_url is None:
        raise RuntimeError("CIVICPLAN_POLICY_DB_URL is not configured.")
    if _policy_repository is None or db_url != _policy_db_url:
        _dispose_policy_repository()
        _policy_db_url = db_url
        _policy_repository = PlanPolicyRepository(db_url=db_url)
    return _policy_repository


def _dispose_policy_repository() -> None:
    global _policy_repository
    if _policy_repository is not None:
        _policy_repository.engine.dispose()
        _policy_repository = None


def _require_staff_role(role: str | None, staff_key_header: str | None) -> None:
    _require_staff_key(role=role, staff_key=staff_key_header)


def _lookup_plan_policy(*, topic: str, plan_type: str = "comprehensive"):
    if _policy_database_url() is None:
        return lookup_plan_policy(topic=topic, plan_type=plan_type)
    return _get_policy_repository().lookup_policy(topic=topic, plan_type=plan_type)


def _lookup_plan_policy_with_source(*, topic: str, plan_type: str = "comprehensive"):
    if _policy_database_url() is None:
        return lookup_plan_policy(topic=topic, plan_type=plan_type), "sample"
    return _get_policy_repository().lookup_policy_with_source(topic=topic, plan_type=plan_type)


def _list_plan_policies(*, plan_type: str | None = None) -> tuple[PlanPolicy, ...]:
    if _policy_database_url() is None:
        policies = tuple(lookup_plan_policy(topic=key) for key in ("housing", "transportation", "parks"))
        if plan_type is None:
            return policies
        return tuple(policy for policy in policies if policy.plan_type == plan_type.strip().casefold())
    return _get_policy_repository().list_policies(plan_type=plan_type)


def _zoning_context_topic(request: ZoningPolicyContextRequest) -> str:
    parts = [request.topic]
    if request.use:
        parts.append(request.use)
    if request.zone_code:
        parts.append(request.zone_code)
    if request.address:
        parts.append(request.address)
    if request.parcel_number:
        parts.append(request.parcel_number)
    return " ".join(part.strip() for part in parts if part and part.strip())


def _stored_staff_analysis_response(stored: StoredStaffAnalysis) -> dict[str, object]:
    return {
        "analysis_id": stored.analysis_id,
        "project_name": stored.project_name,
        "proposal": stored.proposal,
        "policy_id": stored.policy_id,
        "heading": stored.heading,
        "bullets": list(stored.bullets),
        "citations": list(stored.citations),
        "review_required": stored.review_required,
        "disclaimer": stored.disclaimer,
        "created_at": stored.created_at.isoformat(),
    }
