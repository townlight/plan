from datetime import date
from typing import Literal
from pydantic import Field, model_validator
from civicplan.source_bundle import BundleModel


class PolicySelection(BundleModel):
    plan_id: str = Field(min_length=1, max_length=160)
    revision_id: str = Field(min_length=36, max_length=36)
    policy_id: str = Field(min_length=1, max_length=160)


class LinkedSource(BundleModel):
    provider: Literal['meetings', 'zoning']
    source_id: str = Field(min_length=1, max_length=200)
    expected_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    relation: Literal['adoption-evidence', 'hearing', 'context', 'precedent']


class Consideration(BundleModel):
    policy: PolicySelection
    stance: Literal['supporting', 'conflicting', 'uncertain']
    note: str = Field(min_length=1, max_length=5000)


class AnalysisInput(BundleModel):
    expected_previous_revision: str | None = Field(default=None, min_length=36, max_length=36)
    project_name: str = Field(min_length=1, max_length=500)
    proposal: str = Field(min_length=1, max_length=10000)
    selected_policies: list[PolicySelection] = Field(min_length=1, max_length=50)
    considerations: list[Consideration] = Field(default_factory=list, max_length=100)
    analysis_text: str = Field(default='', max_length=50000)
    public_summary: str = Field(default='', max_length=10000)
    staff_notes: str = Field(default='', max_length=10000)
    audience: Literal['staff', 'public'] = 'staff'
    review_state: Literal['draft', 'reviewed'] = 'draft'
    reviewer_label: str = Field(default='', max_length=255)
    reviewed_on: date | None = None
    review_notes: str = Field(default='', max_length=5000)
    linked_sources: list[LinkedSource] = Field(default_factory=list, max_length=50)

    @model_validator(mode='after')
    def valid_review(self):
        if self.review_state == 'reviewed' and not (
            self.reviewer_label and self.reviewed_on and self.review_notes and self.analysis_text
        ):
            raise ValueError('Reviewed analyses require staff text, reviewer, date and review notes.')
        if self.reviewed_on and self.reviewed_on > date.today():
            raise ValueError('A recorded review cannot be in the future.')
        keys = [(p.plan_id, p.revision_id, p.policy_id) for p in self.selected_policies]
        if len(keys) != len(set(keys)):
            raise ValueError('Select each versioned policy once.')
        for consideration in self.considerations:
            p = consideration.policy
            if (p.plan_id, p.revision_id, p.policy_id) not in keys:
                raise ValueError('Every consideration must refer to a selected policy.')
        return self
