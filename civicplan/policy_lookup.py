"""Deterministic comprehensive-plan policy lookup helpers for Townlight Planning."""

from __future__ import annotations

from dataclasses import dataclass


DISCLAIMER = (
    "Townlight Planning provides cited planning-support information only. It does not make "
    "land-use determinations, grant entitlements, or replace planner, attorney, or "
    "elected-official judgment."
)


@dataclass(frozen=True)
class PlanPolicy:
    policy_id: str
    plan_type: str
    title: str
    citation: str
    excerpt: str
    relevance: str
    disclaimer: str = DISCLAIMER


POLICIES = {
    "housing": PlanPolicy(
        policy_id="comp-plan-housing-2.1",
        plan_type="comprehensive",
        title="Missing-middle housing near services",
        citation="Comprehensive Plan, Housing Element, Policy H-2.1",
        excerpt=(
            "Encourage missing-middle housing within walking distance of transit, schools, "
            "parks, and daily services while preserving adopted neighborhood design standards."
        ),
        relevance="Relevant when a proposal adds duplex, triplex, cottage, or small multifamily homes.",
    ),
    "transportation": PlanPolicy(
        policy_id="transportation-plan-3.4",
        plan_type="transportation",
        title="Complete-streets safety corridor",
        citation="Transportation Plan, Mobility Chapter, Policy M-3.4",
        excerpt=(
            "Prioritize pedestrian crossings, traffic calming, and accessible sidewalks on "
            "corridors serving schools, senior housing, civic buildings, and transit stops."
        ),
        relevance="Relevant when a proposal changes street design, access, or pedestrian circulation.",
    ),
    "parks": PlanPolicy(
        policy_id="parks-plan-1.2",
        plan_type="parks",
        title="Ten-minute access to neighborhood parks",
        citation="Parks Plan, Access Chapter, Policy P-1.2",
        excerpt=(
            "Invest in park access so residents can reach a safe neighborhood park or civic "
            "open space within a ten-minute walk where feasible."
        ),
        relevance="Relevant when a proposal affects open space, trails, recreation, or park impact analysis.",
    ),
}


def lookup_plan_policy(*, topic: str, plan_type: str = "comprehensive") -> PlanPolicy:
    """Return a cited sample policy for a planning topic without live search or LLM calls."""

    normalized_topic = topic.strip().casefold()
    normalized_plan = plan_type.strip().casefold()
    for key, policy in POLICIES.items():
        if key in normalized_topic or policy.plan_type == normalized_plan:
            return policy
    return PlanPolicy(
        policy_id="comp-plan-general-1.1",
        plan_type="comprehensive",
        title="General plan consistency review",
        citation="Comprehensive Plan, Introduction, Policy G-1.1",
        excerpt=(
            "Evaluate public and private development actions for consistency with adopted "
            "goals, policies, implementation actions, and capital priorities."
        ),
        relevance="Use as a starting point when no narrower sample policy matches.",
    )
