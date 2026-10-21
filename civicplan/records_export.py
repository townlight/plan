"""Records-ready export helpers for Townlight Planning."""

from __future__ import annotations

from dataclasses import dataclass

from civicplan.policy_lookup import lookup_plan_policy


@dataclass(frozen=True)
class PolicyExport:
    title: str
    policy_id: str
    format: str
    checklist: tuple[str, ...]
    retention_note: str


def build_policy_export(*, title: str, policy_id: str, format: str = "markdown") -> PolicyExport:
    """Build a deterministic records-ready policy-analysis export checklist."""

    policy = lookup_plan_policy(topic=policy_id)
    return PolicyExport(
        title=title.strip() or "Untitled plan-policy export",
        policy_id=policy_id or policy.policy_id,
        format=format,
        checklist=(
            "Preserve source plan citation and excerpt.",
            "Preserve proposal text reviewed by staff.",
            "Record planner reviewer and date before using in an official staff report.",
            "Include the non-determination disclaimer with any public-facing export.",
        ),
        retention_note=(
            "Keep source policy, proposal text, staff reviewer, generated outline, and final "
            "staff edits with the municipal planning record."
        ),
    )
