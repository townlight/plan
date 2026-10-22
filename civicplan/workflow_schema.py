"""Planning analysis/snapshot storage; append-only versions with mutable heads."""
import sqlalchemy as sa

metadata = sa.MetaData(schema='civicplan')
analyses = sa.Table('workflow_analyses', metadata,
    sa.Column('analysis_id', sa.String(36), primary_key=True),
    sa.Column('latest_revision_id', sa.String(36), nullable=False))
versions = sa.Table('workflow_analysis_revisions', metadata,
    sa.Column('revision_id', sa.String(36), primary_key=True),
    sa.Column('analysis_id', sa.String(36), sa.ForeignKey(analyses.c.analysis_id), nullable=False),
    sa.Column('parent_revision_id', sa.String(36)),
    sa.Column('payload', sa.JSON, nullable=False),
    sa.Column('sha256', sa.String(64), nullable=False),
    sa.Column('actor_id', sa.String(255), nullable=False),
    sa.Column('created_at', sa.String(40), nullable=False))
snapshots = sa.Table('workflow_snapshots', metadata,
    sa.Column('snapshot_id', sa.String(36), primary_key=True),
    sa.Column('analysis_id', sa.String(36), sa.ForeignKey(analyses.c.analysis_id), nullable=False),
    sa.Column('analysis_revision_id', sa.String(36), sa.ForeignKey(versions.c.revision_id), nullable=False),
    sa.Column('visibility', sa.String(20), nullable=False),
    sa.Column('text', sa.Text, nullable=False),
    sa.Column('sha256', sa.String(64), nullable=False),
    sa.Column('actor_id', sa.String(255), nullable=False),
    sa.Column('created_at', sa.String(40), nullable=False),
    sa.CheckConstraint("visibility IN ('public','staff_only')"))
events = sa.Table('workflow_audit_events', metadata,
    sa.Column('event_id', sa.String(36), primary_key=True),
    sa.Column('analysis_id', sa.String(36), sa.ForeignKey(analyses.c.analysis_id), nullable=False),
    sa.Column('sequence', sa.Integer, nullable=False),
    sa.Column('previous_hash', sa.String(64), nullable=False),
    sa.Column('entry_hash', sa.String(64), nullable=False),
    sa.Column('timestamp', sa.String(40), nullable=False),
    sa.Column('actor_id', sa.String(255), nullable=False),
    sa.Column('action', sa.String(100), nullable=False),
    sa.Column('details', sa.JSON, nullable=False),
    sa.UniqueConstraint('analysis_id', 'sequence'))
IMMUTABLE_TABLES = (versions, snapshots, events)
