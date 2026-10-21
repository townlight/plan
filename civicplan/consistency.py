"""Plan-policy consistency helpers for Townlight Planning."""

from __future__ import annotations

from dataclasses import dataclass

from civicplan.policy_lookup import DISCLAIMER, lookup_plan_policy


@dataclass(frozen=True)
class ConsistencyCheck:
    policy_id: str
    status: str
    factors: tuple[str, ...]
    staff_next_step: str
    disclaimer: str = DISCLAIMER


def check_policy_consistency(*, proposal: str, policy_id: str) -> ConsistencyCheck:
    """Return deterministic sample consistency support; never an official determination."""

    text = proposal.casefold()
    factors: list[str] = []
    if any(term in text for term in ("transit", "sidewalk", "walk", "bike", "school")):
        factors.append("Proposal references access, mobility, or proximity to civic services.")
    if any(term in text for term in ("housing", "duplex", "apartment", "mixed-use")):
        factors.append("Proposal references housing choice or mixed-use development.")
    if any(term in text for term in ("park", "trail", "open space", "recreation")):
        factors.append("Proposal references parks, trails, or public open space.")
    if not factors:
        factors.append("No obvious sample-policy keyword match; planner review is required.")

    status = "potentially-consistent" if len(factors) > 1 else "needs-planner-review"
    policy = lookup_plan_policy(topic=policy_id)
    return ConsistencyCheck(
        policy_id=policy_id or policy.policy_id,
        status=status,
        factors=tuple(factors),
        staff_next_step=(
            "Attach cited plan policies to the staff report and route to the planner of record "
            "for official consistency findings."
        ),
    )
