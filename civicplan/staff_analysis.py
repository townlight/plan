"""Staff-analysis outline helpers for Townlight Planning."""

from __future__ import annotations

from dataclasses import dataclass

from civicplan.consistency import check_policy_consistency
from civicplan.policy_lookup import DISCLAIMER, lookup_plan_policy


@dataclass(frozen=True)
class StaffAnalysisDraft:
    project_name: str
    heading: str
    bullets: tuple[str, ...]
    citations: tuple[str, ...]
    review_required: bool
    disclaimer: str = DISCLAIMER


def draft_staff_analysis(*, project_name: str, proposal: str, policy_id: str) -> StaffAnalysisDraft:
    """Create a deterministic cited outline for a staff report section."""

    policy = lookup_plan_policy(topic=policy_id)
    consistency = check_policy_consistency(proposal=proposal, policy_id=policy_id)
    clean_name = project_name.strip() or "Untitled planning item"
    return StaffAnalysisDraft(
        project_name=clean_name,
        heading=f"Plan consistency context for {clean_name}",
        bullets=(
            f"Relevant adopted policy: {policy.title}.",
            f"Sample consistency status: {consistency.status}.",
            "Planner of record must confirm facts, local procedures, noticing requirements, and official findings.",
        ),
        citations=(policy.citation,),
        review_required=True,
    )
