"""Append-only plan sources; preserve all legacy policy and analysis tables."""

from alembic import op
import sqlalchemy as sa

from townlight_planning.source_schema import IMMUTABLE_TABLES, metadata
from townlight_planning.persistence import metadata as legacy_metadata

revision = "townlight_planning_0001"
down_revision = None


def upgrade():
    connection = op.get_bind()
    legacy_metadata.create_all(connection)
    metadata.create_all(connection)
    if connection.dialect.name == "postgresql":
        connection.execute(sa.text("""
            CREATE FUNCTION townlight_planning.reject_source_mutation() RETURNS trigger
            LANGUAGE plpgsql AS $$ BEGIN
                RAISE EXCEPTION 'Planning source history is append-only';
            END $$
        """))
        for table in IMMUTABLE_TABLES:
            connection.execute(sa.text(
                f"CREATE TRIGGER immutable_source BEFORE UPDATE OR DELETE ON townlight_planning.{table.name} "
                "FOR EACH ROW EXECUTE FUNCTION townlight_planning.reject_source_mutation()"
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
