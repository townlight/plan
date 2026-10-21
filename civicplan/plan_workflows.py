from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal

from civicplan.policy_lookup import DISCLAIMER, POLICIES, PlanPolicy, lookup_plan_policy


PlanStatus = Literal["adopted", "pending", "superseded"]


@dataclass(frozen=True)
class PlanPolicyIngestRecord:
    topic_key: str
    policy: PlanPolicy
    adoption_status: PlanStatus
    source_document: str


@dataclass(frozen=True)
class PlanQuestionAnswer:
    status: str
    answer: str
    citations: tuple[str, ...]
    source_policy_ids: tuple[str, ...]
    review_required: bool
    disclaimer: str = DISCLAIMER


@dataclass(frozen=True)
class PlanAmendment:
    amendment_id: str
    plan_type: str
    title: str
    adoption_status: PlanStatus
    adopted_date: str | None
    citation: str
    summary: str


@dataclass(frozen=True)
class ProgressTarget:
    target_id: str
    policy_id: str
    metric: str
    status: str
    evidence: str
    citation: str
    updated_at: datetime


SAMPLE_AMENDMENTS = (
    PlanAmendment(
        amendment_id="amd-2024-housing-element",
        plan_type="comprehensive",
        title="Housing Element update",
        adoption_status="adopted",
        adopted_date="2024-09-10",
        citation="Ordinance 2024-18; Comprehensive Plan Housing Element",
        summary="Adds missing-middle housing policy language near transit, schools, parks, and services.",
    ),
    PlanAmendment(
        amendment_id="amd-2026-corridor-study",
        plan_type="small-area",
        title="North Corridor small-area plan",
        adoption_status="pending",
        adopted_date=None,
        citation="Planning Commission draft minutes, 2026-03-12",
        summary="Pending corridor policies must be labeled as draft and not treated as adopted plan text.",
    ),
)

SAMPLE_PROGRESS_TARGETS = (
    ProgressTarget(
        target_id="target-housing-services",
        policy_id="comp-plan-housing-2.1",
        metric="Share of new missing-middle units within walking distance of daily services.",
        status="needs_evidence",
        evidence="No adopted annual progress report loaded in the local dataset.",
        citation="Comprehensive Plan, Housing Element, Policy H-2.1",
        updated_at=datetime(2026, 5, 7, tzinfo=UTC),
    ),
    ProgressTarget(
        target_id="target-parks-access",
        policy_id="parks-plan-1.2",
        metric="Residents within a ten-minute walk of a neighborhood park or civic open space.",
        status="on_track",
        evidence="Sample parks access inventory marks the downtown and school-adjacent areas as served.",
        citation="Parks Plan, Access Chapter, Policy P-1.2",
        updated_at=datetime(2026, 5, 7, tzinfo=UTC),
    ),
)


def normalize_ingested_policy(
    *,
    topic_key: str,
    policy_id: str,
    plan_type: str,
    title: str,
    citation: str,
    excerpt: str,
    relevance: str,
    adoption_status: str,
    source_document: str,
) -> PlanPolicyIngestRecord:
    status = adoption_status.strip().casefold()
    if status not in {"adopted", "pending", "superseded"}:
        raise ValueError("adoption_status must be adopted, pending, or superseded.")
    if status != "adopted":
        relevance = f"{relevance} This policy is {status} and requires staff confirmation before reliance."
    return PlanPolicyIngestRecord(
        topic_key=topic_key,
        policy=PlanPolicy(
            policy_id=policy_id.strip(),
            plan_type=plan_type.strip().casefold(),
            title=title.strip(),
            citation=citation.strip(),
            excerpt=excerpt.strip(),
            relevance=relevance.strip(),
        ),
        adoption_status=status,  # type: ignore[arg-type]
        source_document=source_document.strip(),
    )


def plan_navigator(policies: tuple[PlanPolicy, ...] | None = None) -> dict[str, object]:
    records = tuple(POLICIES.values()) if policies is None else policies
    grouped: dict[str, list[dict[str, str]]] = {}
    for policy in records:
        grouped.setdefault(policy.plan_type, []).append(
            {
                "policy_id": policy.policy_id,
                "title": policy.title,
                "citation": policy.citation,
                "excerpt": policy.excerpt,
            }
        )
    return {
        "plans": [
            {"plan_type": plan_type, "policies": sorted(items, key=lambda item: item["policy_id"])}
            for plan_type, items in sorted(grouped.items())
        ],
        "boundary": "Navigator shows cited plan structure only; staff verify applicability before decisions.",
    }


def answer_plan_question(
    *,
    question: str,
    plan_type: str = "comprehensive",
    policies: tuple[PlanPolicy, ...] | None = None,
) -> PlanQuestionAnswer:
    normalized = question.casefold()
    candidates = tuple(POLICIES.values()) if policies is None else policies
    matches = tuple(
        policy
        for policy in candidates
        if policy.plan_type == plan_type.casefold()
        and (
            policy.policy_id.casefold() in normalized
            or any(word in normalized for word in _topic_words(policy))
        )
    )
    if not matches and policies is None:
        fallback = lookup_plan_policy(topic=question, plan_type=plan_type)
        matches = (fallback,)
    citations = tuple(policy.citation for policy in matches)
    answer = " ".join(
        f"{policy.title}: {policy.excerpt} Relevance: {policy.relevance}" for policy in matches
    )
    return PlanQuestionAnswer(
        status="answered" if matches else "no_supported_policy",
        answer=answer,
        citations=citations,
        source_policy_ids=tuple(policy.policy_id for policy in matches),
        review_required=True,
    )


def synthesize_plan_context(*, topic: str, policies: tuple[PlanPolicy, ...] | None = None) -> dict[str, object]:
    candidates = tuple(POLICIES.values()) if policies is None else policies
    matched = tuple(
        policy
        for policy in candidates
        if any(word in topic.casefold() for word in _topic_words(policy))
    )
    return {
        "topic": topic,
        "summary": " ".join(policy.relevance for policy in matched),
        "citations": [policy.citation for policy in matched],
        "source_policy_ids": [policy.policy_id for policy in matched],
        "review_required": True,
        "disclaimer": DISCLAIMER,
    }


def amendment_history(*, plan_type: str | None = None) -> tuple[PlanAmendment, ...]:
    if plan_type is None:
        return SAMPLE_AMENDMENTS
    return tuple(
        amendment for amendment in SAMPLE_AMENDMENTS if amendment.plan_type == plan_type.casefold()
    )


def progress_targets(*, policy_id: str | None = None) -> tuple[ProgressTarget, ...]:
    if policy_id is None:
        return SAMPLE_PROGRESS_TARGETS
    return tuple(target for target in SAMPLE_PROGRESS_TARGETS if target.policy_id == policy_id)


def civicclerk_staff_report_context(*, agenda_item: str, topic: str) -> dict[str, object]:
    answer = answer_plan_question(question=topic)
    return {
        "agenda_item": agenda_item,
        "policy_context": answer.answer,
        "citations": list(answer.citations),
        "review_required": True,
        "boundary": (
            "Townlight Planning provides staff-report context for Townlight Meetings; the staff report remains "
            "draft-only until reviewed by planning staff."
        ),
    }


def _topic_words(policy: PlanPolicy) -> tuple[str, ...]:
    return tuple(
        word
        for word in (policy.title + " " + policy.excerpt + " " + policy.relevance).casefold().split()
        if len(word) > 5
    )
