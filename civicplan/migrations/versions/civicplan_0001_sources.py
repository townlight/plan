"""Append-only plan sources; preserve all legacy policy and analysis tables."""

from alembic import op
import sqlalchemy as sa

from civicplan.source_schema import IMMUTABLE_TABLES, metadata
from civicplan.persistence import metadata as legacy_metadata

revision = "civicplan_0001"
down_revision = None


def upgrade():
    connection = op.get_bind()
    legacy_metadata.create_all(connection)
    metadata.create_all(connection)
    if connection.dialect.name == "postgresql":
        connection.execute(sa.text("""
            CREATE FUNCTION civicplan.reject_source_mutation() RETURNS trigger
            LANGUAGE plpgsql AS $$ BEGIN
                RAISE EXCEPTION 'Planning source history is append-only';
            END $$
        """))
        for table in IMMUTABLE_TABLES:
            connection.execute(sa.text(
                f"CREATE TRIGGER immutable_source BEFORE UPDATE OR DELETE ON civicplan.{table.name} "
                "FOR EACH ROW EXECUTE FUNCTION civicplan.reject_source_mutation()"
            ))
    else:
        for table in IMMUTABLE_TABLES:
            for operation in ("UPDATE", "DELETE"):
                connection.execute(sa.text(
                    f"CREATE TRIGGER {table.name}_{operation.lower()} BEFORE {operation} "
                    f"ON {table.name} BEGIN SELECT RAISE(ABORT, 'Planning source history is append-only'); END"
                ))


def downgrade():
    raise RuntimeError("Destructive source-history downgrade is unsupported; restore a verified backup.")
