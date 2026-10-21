"""Planning-owned source schema. DDL is applied only by explicit migrations."""

import sqlalchemy as sa

metadata = sa.MetaData(schema="civicplan")

plans = sa.Table(
    "source_plans", metadata,
    sa.Column("plan_id", sa.String(160), primary_key=True),
    sa.Column("latest_revision_id", sa.String(36), nullable=False),
)
revisions = sa.Table(
    "source_revisions", metadata,
    sa.Column("revision_id", sa.String(36), primary_key=True),
    sa.Column("plan_id", sa.String(160), sa.ForeignKey(plans.c.plan_id), nullable=False),
    sa.Column("parent_revision_id", sa.String(36), sa.ForeignKey("civicplan.source_revisions.revision_id")),
    sa.Column("sequence", sa.Integer, nullable=False),
    sa.Column("bundle_sha256", sa.String(64), nullable=False),
    sa.Column("title", sa.String(500), nullable=False),
    sa.Column("jurisdiction", sa.String(255), nullable=False),
    sa.Column("plan_type", sa.String(40), nullable=False),
    sa.Column("status", sa.String(20), nullable=False),
    sa.Column("visibility", sa.String(20), nullable=False),
    sa.Column("dataset_kind", sa.String(20), nullable=False),
    sa.Column("source_date", sa.Date, nullable=False),
    sa.Column("adopted_on", sa.Date),
    sa.Column("effective_on", sa.Date),
    sa.Column("change_note", sa.Text, nullable=False),
    sa.Column("reviewer_label", sa.String(255), nullable=False),
    sa.Column("actor_id", sa.String(255), nullable=False),
    sa.Column("created_at", sa.String(40), nullable=False),
    sa.UniqueConstraint("plan_id", "bundle_sha256"),
    sa.UniqueConstraint("plan_id", "sequence"),
    sa.CheckConstraint("status IN ('pending', 'adopted', 'superseded')"),
    sa.CheckConstraint("visibility IN ('staff', 'public')"),
)
documents = sa.Table(
    "source_documents", metadata,
    sa.Column("revision_id", sa.String(36), sa.ForeignKey(revisions.c.revision_id), primary_key=True),
    sa.Column("document_id", sa.String(160), primary_key=True),
    sa.Column("filename", sa.String(255), nullable=False),
    sa.Column("media_type", sa.String(120), nullable=False),
    sa.Column("sha256", sa.String(64), nullable=False),
    sa.Column("original_bytes", sa.LargeBinary, nullable=False),
)
policies = sa.Table(
    "source_policies", metadata,
    sa.Column("revision_id", sa.String(36), primary_key=True),
    sa.Column("policy_id", sa.String(160), primary_key=True),
    sa.Column("document_id", sa.String(160), nullable=False),
    sa.Column("goal", sa.String(500), nullable=False),
    sa.Column("objective", sa.String(500), nullable=False),
    sa.Column("topic_key", sa.String(160), nullable=False),
    sa.Column("title", sa.String(500), nullable=False),
    sa.Column("citation", sa.String(500), nullable=False),
    sa.Column("anchor", sa.String(500), nullable=False),
    sa.Column("excerpt", sa.Text, nullable=False),
    sa.Column("relevance", sa.Text, nullable=False),
    sa.ForeignKeyConstraint(
        ["revision_id", "document_id"],
        [documents.c.revision_id, documents.c.document_id],
    ),
)
evidence = sa.Table(
    "source_adoption_evidence", metadata,
    sa.Column("revision_id", sa.String(36), sa.ForeignKey(revisions.c.revision_id), primary_key=True),
    sa.Column("ordinal", sa.Integer, primary_key=True),
    sa.Column("kind", sa.String(40), nullable=False),
    sa.Column("reference", sa.String(1000), nullable=False),
    sa.Column("document_id", sa.String(160)),
    sa.Column("note", sa.Text, nullable=False),
    sa.ForeignKeyConstraint(
        ["revision_id", "document_id"],
        [documents.c.revision_id, documents.c.document_id],
    ),
)
events = sa.Table(
    "source_audit_events", metadata,
    sa.Column("revision_id", sa.String(36), sa.ForeignKey(revisions.c.revision_id), primary_key=True),
    sa.Column("plan_id", sa.String(160), nullable=False),
    sa.Column("sequence", sa.Integer, nullable=False),
    sa.Column("previous_hash", sa.String(64), nullable=False),
    sa.Column("entry_hash", sa.String(64), nullable=False),
    sa.Column("timestamp", sa.String(40), nullable=False),
    sa.Column("actor_id", sa.String(255), nullable=False),
    sa.Column("action", sa.String(80), nullable=False),
    sa.Column("details", sa.JSON, nullable=False),
    sa.UniqueConstraint("plan_id", "sequence"),
)

IMMUTABLE_TABLES = (revisions, documents, policies, evidence, events)
