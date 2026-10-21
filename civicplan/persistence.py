from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civicplan.policy_lookup import POLICIES, PlanPolicy, lookup_plan_policy
from civicplan.staff_analysis import draft_staff_analysis


metadata = sa.MetaData()

plan_policy_records = sa.Table(
    "plan_policy_records",
    metadata,
    sa.Column("policy_id", sa.String(160), primary_key=True),
    sa.Column("plan_type", sa.String(120), nullable=False),
    sa.Column("topic_key", sa.String(160), nullable=False),
    sa.Column("title", sa.String(500), nullable=False),
    sa.Column("citation", sa.String(500), nullable=False),
    sa.Column("excerpt", sa.Text(), nullable=False),
    sa.Column("relevance", sa.Text(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicplan",
)

staff_analysis_records = sa.Table(
    "staff_analysis_records",
    metadata,
    sa.Column("analysis_id", sa.String(36), primary_key=True),
    sa.Column("project_name", sa.String(500), nullable=False),
    sa.Column("proposal", sa.Text(), nullable=False),
    sa.Column("policy_id", sa.String(160), nullable=False),
    sa.Column("heading", sa.String(500), nullable=False),
    sa.Column("bullets", sa.JSON(), nullable=False),
    sa.Column("citations", sa.JSON(), nullable=False),
    sa.Column("review_required", sa.Boolean(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicplan",
)


@dataclass(frozen=True)
class StoredStaffAnalysis:
    analysis_id: str
    project_name: str
    proposal: str
    policy_id: str
    heading: str
    bullets: tuple[str, ...]
    citations: tuple[str, ...]
    review_required: bool
    disclaimer: str
    created_at: datetime


class PlanPolicyRepository:
    """SQLAlchemy-backed policy and staff-analysis records for local planning workflows."""

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None,
                 seed_defaults: bool = False, initialize: bool = False) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civicplan": None})
        else:
            self.engine = base_engine
        if initialize:
            with self.engine.begin() as connection:
                if self.engine.dialect.name == "postgresql":
                    connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civicplan"))
            metadata.create_all(self.engine)
        if seed_defaults:
            self.seed_policies(POLICIES.items())

    def seed_policies(self, policies: Iterable[tuple[str, PlanPolicy]]) -> None:
        now = datetime.now(UTC)
        with self.engine.begin() as connection:
            for topic_key, policy in policies:
                exists = connection.execute(
                    sa.select(plan_policy_records.c.policy_id).where(
                        plan_policy_records.c.policy_id == policy.policy_id
                    )
                ).first()
                if exists is not None:
                    continue
                connection.execute(
                    plan_policy_records.insert().values(
                        policy_id=policy.policy_id,
                        plan_type=policy.plan_type,
                        topic_key=topic_key.casefold(),
                        title=policy.title,
                        citation=policy.citation,
                        excerpt=policy.excerpt,
                        relevance=policy.relevance,
                        disclaimer=policy.disclaimer,
                        created_at=now,
                        updated_at=now,
                    )
                )

    def lookup_policy(self, *, topic: str, plan_type: str = "comprehensive") -> PlanPolicy:
        policy, _source = self.lookup_policy_with_source(topic=topic, plan_type=plan_type)
        return policy

    def upsert_policy(self, *, topic_key: str, policy: PlanPolicy) -> PlanPolicy:
        now = datetime.now(UTC)
        normalized_topic = topic_key.strip().casefold()
        if not normalized_topic:
            raise ValueError("topic_key is required for plan-policy ingestion.")
        with self.engine.begin() as connection:
            existing = connection.execute(
                sa.select(plan_policy_records.c.policy_id).where(
                    plan_policy_records.c.policy_id == policy.policy_id
                )
            ).first()
            values = {
                "policy_id": policy.policy_id,
                "plan_type": policy.plan_type,
                "topic_key": normalized_topic,
                "title": policy.title,
                "citation": policy.citation,
                "excerpt": policy.excerpt,
                "relevance": policy.relevance,
                "disclaimer": policy.disclaimer,
                "updated_at": now,
            }
            if existing is None:
                connection.execute(
                    plan_policy_records.insert().values(**values, created_at=now)
                )
            else:
                connection.execute(
                    plan_policy_records.update()
                    .where(plan_policy_records.c.policy_id == policy.policy_id)
                    .values(**values)
                )
        return policy

    def list_policies(self, *, plan_type: str | None = None) -> tuple[PlanPolicy, ...]:
        with self.engine.begin() as connection:
            statement = sa.select(plan_policy_records).order_by(
                plan_policy_records.c.plan_type,
                plan_policy_records.c.policy_id,
            )
            if plan_type:
                statement = statement.where(
                    sa.func.lower(plan_policy_records.c.plan_type) == plan_type.strip().casefold()
                )
            rows = connection.execute(statement).mappings().all()
        return tuple(_row_to_policy(row) for row in rows)

    def lookup_policy_with_source(
        self, *, topic: str, plan_type: str = "comprehensive"
    ) -> tuple[PlanPolicy, str]:
        normalized_topic = topic.strip().casefold()
        normalized_plan = plan_type.strip().casefold()
        with self.engine.begin() as connection:
            rows = connection.execute(
                sa.select(plan_policy_records).where(
                    sa.func.lower(plan_policy_records.c.plan_type) == normalized_plan
                )
            ).mappings().all()
        for row in rows:
            topic_key = str(row["topic_key"]).casefold()
            policy_id = str(row["policy_id"]).casefold()
            if topic_key in normalized_topic or policy_id == normalized_topic:
                return _row_to_policy(row), "persisted"
        return lookup_plan_policy(topic=topic, plan_type=plan_type), "sample"

    def create_staff_analysis(
        self, *, project_name: str, proposal: str, policy_id: str
    ) -> StoredStaffAnalysis:
        draft = draft_staff_analysis(
            project_name=project_name,
            proposal=proposal,
            policy_id=policy_id,
        )
        stored = StoredStaffAnalysis(
            analysis_id=str(uuid4()),
            project_name=draft.project_name,
            proposal=proposal,
            policy_id=policy_id,
            heading=draft.heading,
            bullets=draft.bullets,
            citations=draft.citations,
            review_required=draft.review_required,
            disclaimer=draft.disclaimer,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                staff_analysis_records.insert().values(
                    analysis_id=stored.analysis_id,
                    project_name=stored.project_name,
                    proposal=stored.proposal,
                    policy_id=stored.policy_id,
                    heading=stored.heading,
                    bullets=list(stored.bullets),
                    citations=list(stored.citations),
                    review_required=stored.review_required,
                    disclaimer=stored.disclaimer,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_staff_analysis(self, analysis_id: str) -> StoredStaffAnalysis | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(staff_analysis_records).where(
                    staff_analysis_records.c.analysis_id == analysis_id
                )
            ).mappings().first()
        if row is None:
            return None
        return _row_to_staff_analysis(row)


def _row_to_policy(row: object) -> PlanPolicy:
    data = dict(row)
    return PlanPolicy(
        policy_id=data["policy_id"],
        plan_type=data["plan_type"],
        title=data["title"],
        citation=data["citation"],
        excerpt=data["excerpt"],
        relevance=data["relevance"],
        disclaimer=data["disclaimer"],
    )


def _row_to_staff_analysis(row: object) -> StoredStaffAnalysis:
    data = dict(row)
    return StoredStaffAnalysis(
        analysis_id=data["analysis_id"],
        project_name=data["project_name"],
        proposal=data["proposal"],
        policy_id=data["policy_id"],
        heading=data["heading"],
        bullets=tuple(data["bullets"]),
        citations=tuple(data["citations"]),
        review_required=data["review_required"],
        disclaimer=data["disclaimer"],
        created_at=data["created_at"],
    )
