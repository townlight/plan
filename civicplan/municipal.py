# SPDX-License-Identifier: AGPL-3.0-only
"""Persistent municipal initiatives and amendment workflow, separate from plan adoption."""

from datetime import date, datetime, UTC
from decimal import Decimal
import hashlib
import json
from typing import Literal
from uuid import uuid4

import sqlalchemy as sa
from pydantic import Field, model_validator
from civicplan.source_bundle import BundleModel
from civicplan.workflow_models import PolicySelection
from civicplan.policy_service import PolicyService
from civicplan.source_store import SourceConflict

metadata = sa.MetaData(schema="civicplan")
items = sa.Table(
    "municipal_items",
    metadata,
    sa.Column("item_id", sa.String(36), primary_key=True),
    sa.Column("kind", sa.String(20), nullable=False),
    sa.Column("head_revision", sa.String(36), nullable=False),
)
revisions = sa.Table(
    "municipal_revisions",
    metadata,
    sa.Column("revision_id", sa.String(36), primary_key=True),
    sa.Column("item_id", sa.String(36), sa.ForeignKey(items.c.item_id), nullable=False),
    sa.Column("sequence", sa.Integer, nullable=False),
    sa.Column("previous_hash", sa.String(64), nullable=False),
    sa.Column("sha256", sa.String(64), nullable=False),
    sa.Column("actor_id", sa.String(255), nullable=False),
    sa.Column("created_at", sa.String(40), nullable=False),
    sa.Column("snapshot", sa.JSON, nullable=False),
    sa.UniqueConstraint("item_id", "sequence"),
)


class Measurement(BundleModel):
    recorded_on: date
    value: Decimal = Field(allow_inf_nan=False)
    evidence: str = Field(min_length=1, max_length=2000)

    @model_validator(mode="after")
    def past(self):
        if self.recorded_on > date.today():
            raise ValueError("A measurement cannot be recorded in the future")
        return self


class Milestone(BundleModel):
    title: str = Field(min_length=1, max_length=255)
    due_on: date
    completed_on: date | None = None
    evidence: str = Field(default="", max_length=2000)

    @model_validator(mode="after")
    def completed(self):
        if self.completed_on and (self.completed_on > date.today() or not self.evidence):
            raise ValueError("Completed milestones need evidence and a nonfuture date")
        return self


class InitiativeInput(BundleModel):
    expected_revision: str | None = Field(default=None, min_length=36, max_length=36)
    title: str = Field(min_length=1, max_length=500)
    policy: PolicySelection
    responsible_staff: str = Field(min_length=1, max_length=255)
    target: Decimal = Field(allow_inf_nan=False)
    unit: str = Field(min_length=1, max_length=80)
    due_on: date
    status: Literal["planned", "active", "completed", "cancelled"] = "planned"
    milestones: list[Milestone] = Field(default_factory=list, max_length=100)
    measurements: list[Measurement] = Field(default_factory=list, max_length=1000)
    note: str = Field(min_length=1, max_length=5000)

    @model_validator(mode="after")
    def completion(self):
        if self.status == "completed" and (
            not self.measurements or any(m.completed_on is None for m in self.milestones)
        ):
            raise ValueError(
                "Completed initiatives need measurement evidence and completed milestones"
            )
        return self


class AmendmentInput(BundleModel):
    expected_revision: str | None = Field(default=None, min_length=36, max_length=36)
    title: str = Field(min_length=1, max_length=500)
    policy: PolicySelection
    proposal: str = Field(min_length=1, max_length=20000)
    responsible_staff: str = Field(min_length=1, max_length=255)
    status: Literal["draft", "review", "adopted", "withdrawn"] = "draft"
    review_note: str = Field(default="", max_length=5000)
    adoption_revision: str | None = Field(default=None, min_length=36, max_length=36)
    note: str = Field(min_length=1, max_length=5000)

    @model_validator(mode="after")
    def reviewed(self):
        if self.status in {"review", "adopted"} and not self.review_note:
            raise ValueError("Review and adoption need a recorded review note")
        if (self.status == "adopted") != (self.adoption_revision is not None):
            raise ValueError("Only an adopted amendment references an imported adoption revision")
        return self


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


class MunicipalRepository:
    def __init__(self, sources):
        self.sources = sources
        self.engine = sources.engine

    def save(self, data, actor, item_id=None):
        if not actor or len(actor) > 255:
            raise ValueError("Authenticated actor required")
        kind = "initiative" if isinstance(data, InitiativeInput) else "amendment"
        creating = item_id is None
        if creating != (data.expected_revision is None):
            raise ValueError("Updates require the current revision; new items have none")
        item_id = item_id or str(uuid4())
        policy = PolicyService(self.sources).resolve(
            data.policy.revision_id, data.policy.policy_id, staff=True
        )
        if policy["plan_id"] != data.policy.plan_id:
            raise ValueError("Selected policy belongs to another plan")
        if not self.sources.verify_sources(data.policy.plan_id)["ok"]:
            raise ValueError("Plan source integrity failed")
        adoption = None
        if kind == "amendment" and data.status == "adopted":
            adoption = self.sources.revision(data.adoption_revision, staff=True)
            base = self.sources.revision(data.policy.revision_id, staff=True)
            if (
                not adoption
                or adoption["plan_id"] != data.policy.plan_id
                or (adoption["status"] != "adopted" or adoption["sequence"] <= base["sequence"])
            ):
                raise ValueError("Adoption requires a later adopted source revision of this plan")
            # Imported source records retain the actual adoption evidence; no plan text is changed here.
            if not adoption["adoption_evidence"]:
                raise ValueError("Imported adoption evidence is required")
        snapshot = data.model_dump(mode="json", exclude={"expected_revision"})
        snapshot["source"] = policy
        snapshot["kind"] = kind
        if adoption:
            snapshot["adoption_source"] = {
                key: adoption[key] for key in ("revision_id", "bundle_sha256", "adoption_evidence")
            }
        with self.engine.begin() as conn:
            if conn.dialect.name == "postgresql":
                key = int.from_bytes(
                    hashlib.sha256(("municipal:" + item_id).encode()).digest()[:8],
                    "big",
                    signed=True,
                )
                conn.execute(sa.text("SELECT pg_advisory_xact_lock(:key)"), {"key": key})
            head = (
                conn.execute(sa.select(items).where(items.c.item_id == item_id)).mappings().first()
            )
            if not creating and head is None:
                raise ValueError("Municipal workflow not found")
            previous = None
            if head:
                if head["kind"] != kind or head["head_revision"] != data.expected_revision:
                    raise SourceConflict("Municipal workflow changed; reload before saving")
                previous = (
                    conn.execute(
                        sa.select(revisions).where(revisions.c.revision_id == head["head_revision"])
                    )
                    .mappings()
                    .one()
                )
                prior = previous["snapshot"]
                if kind == "initiative" and prior["measurements"] and prior["unit"] != snapshot["unit"]:
                    raise ValueError("Measurement units are fixed after recording evidence")
                if prior["policy"] != snapshot["policy"]:
                    raise ValueError(
                        "The original policy reference is fixed; create a new workflow"
                    )
                allowed = (
                    {
                        "draft": {"draft", "review", "withdrawn"},
                        "review": {"draft", "review", "adopted", "withdrawn"},
                        "adopted": set(),
                        "withdrawn": set(),
                    }
                    if kind == "amendment"
                    else {
                        "planned": {"planned", "active", "cancelled"},
                        "active": {"active", "completed", "cancelled"},
                        "completed": set(),
                        "cancelled": set(),
                    }
                )
                if data.status not in allowed[prior["status"]]:
                    raise SourceConflict("This lifecycle transition is not allowed")
                if (
                    kind == "initiative"
                    and snapshot["measurements"][: len(prior["measurements"])]
                    != prior["measurements"]
                ):
                    raise ValueError(
                        "Recorded measurements are append-only; record a correction as new evidence"
                    )
            elif data.status != ("planned" if kind == "initiative" else "draft"):
                raise ValueError("Start an initiative as planned or an amendment as draft")
            revision_id = str(uuid4())
            row = dict(
                revision_id=revision_id,
                item_id=item_id,
                sequence=previous["sequence"] + 1 if previous else 1,
                previous_hash=previous["sha256"] if previous else "0" * 64,
                actor_id=actor,
                created_at=datetime.now(UTC).isoformat(),
                snapshot=snapshot,
            )
            row["sha256"] = digest(row)
            if creating:
                conn.execute(
                    items.insert().values(item_id=item_id, kind=kind, head_revision=revision_id)
                )
            else:
                conn.execute(
                    items.update()
                    .where(items.c.item_id == item_id)
                    .values(head_revision=revision_id)
                )
            conn.execute(revisions.insert().values(**row))
        return row

    def history(self, item_id):
        with self.engine.connect() as conn:
            rows = [
                dict(row)
                for row in conn.execute(
                    sa.select(revisions)
                    .where(revisions.c.item_id == item_id)
                    .order_by(revisions.c.sequence)
                ).mappings()
            ]
        previous = "0" * 64
        for sequence, row in enumerate(rows, 1):
            value = {key: val for key, val in row.items() if key != "sha256"}
            if (
                row["sequence"] != sequence
                or row["previous_hash"] != previous
                or digest(value) != row["sha256"]
            ):
                raise SourceConflict("Municipal history integrity failed")
            previous = row["sha256"]
        return rows

    def list(self, kind, *, policy_id=None, plan_type=None, offset=0, limit=50):
        with self.engine.connect() as conn:
            # Filter in SQL before paging so selection never silently loses matches.
            query = (
                sa.select(revisions)
                .join(items, items.c.head_revision == revisions.c.revision_id)
                .where(items.c.kind == kind)
            )
            if policy_id:
                query = query.where(
                    revisions.c.snapshot["policy"]["policy_id"].as_string() == policy_id
                )
            if plan_type:
                query = query.where(
                    revisions.c.snapshot["source"]["plan_type"].as_string() == plan_type
                )
            rows = (
                conn.execute(query.order_by(revisions.c.item_id).offset(offset).limit(limit + 1))
                .mappings()
                .all()
            )
        return {
            "items": [dict(row) for row in rows[:limit]],
            "next_offset": offset + limit if len(rows) > limit else None,
            "boundary": "Staff planning support; source adoption and public release are separate.",
        }
