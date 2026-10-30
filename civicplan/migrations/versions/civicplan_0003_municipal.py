# SPDX-License-Identifier: AGPL-3.0-only
"""Municipal initiative and amendment snapshots; no plan source mutation."""

from alembic import op
import sqlalchemy as sa
from civicplan.municipal import metadata, revisions

revision = "civicplan_0003"
down_revision = "civicplan_0002"


def upgrade():
    conn = op.get_bind()
    metadata.create_all(conn)
    if conn.dialect.name == "postgresql":
        conn.execute(
            sa.text(
                "CREATE TRIGGER immutable_municipal BEFORE UPDATE OR DELETE ON civicplan.municipal_revisions "
                "FOR EACH ROW EXECUTE FUNCTION civicplan.reject_source_mutation()"
            )
        )
    else:
        for operation in ("UPDATE", "DELETE"):
            conn.execute(
                sa.text(
                    f"CREATE TRIGGER municipal_revisions_{operation.lower()} BEFORE {operation} "
                    f"ON {revisions.name} BEGIN SELECT RAISE(ABORT, 'Municipal history is append-only'); END"
                )
            )


def downgrade():
    raise RuntimeError("Destructive municipal downgrade is unsupported; restore a verified backup")
