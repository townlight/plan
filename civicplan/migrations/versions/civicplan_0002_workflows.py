"""Append-only staff analysis and connected source snapshots."""
from alembic import op
import sqlalchemy as sa
from civicplan.workflow_schema import metadata, IMMUTABLE_TABLES

revision = 'civicplan_0002'
down_revision = 'civicplan_0001'


def upgrade():
    conn = op.get_bind()
    metadata.create_all(conn)
    for table in IMMUTABLE_TABLES:
        if conn.dialect.name == 'postgresql':
            conn.execute(sa.text(
                f'CREATE TRIGGER immutable_workflow BEFORE UPDATE OR DELETE ON civicplan.{table.name} '
                'FOR EACH ROW EXECUTE FUNCTION civicplan.reject_source_mutation()'))
        else:
            for operation in ('UPDATE', 'DELETE'):
                conn.execute(sa.text(f'CREATE TRIGGER {table.name}_{operation.lower()} BEFORE {operation} '
                    f"ON {table.name} BEGIN SELECT RAISE(ABORT, 'Planning workflow history is append-only'); END"))


def downgrade():
    raise RuntimeError('Destructive workflow downgrade is unsupported; restore a verified backup.')
