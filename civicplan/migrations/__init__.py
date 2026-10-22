"""Explicit additive Planning migrations; never run by a request handler."""

from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
import sqlalchemy as sa

HEAD = "civicplan_0002"


def source_engine(url: str) -> sa.Engine:
    engine = sa.create_engine(url)
    if engine.dialect.name == "sqlite":
        @sa.event.listens_for(engine, "connect")
        def foreign_keys(connection, _record):
            connection.execute("PRAGMA foreign_keys=ON")
        return engine.execution_options(schema_translate_map={"civicplan": None})
    if engine.dialect.name != "postgresql":
        engine.dispose()
        raise ValueError("Planning sources require PostgreSQL (SQLite is supported for tests).")
    return engine


def upgrade(engine: sa.Engine) -> None:
    config = Config()
    config.set_main_option("script_location", str(Path(__file__).parent))
    with engine.begin() as connection:
        if engine.dialect.name == "postgresql":
            connection.execute(sa.text("SELECT pg_advisory_xact_lock(80400001)"))
            connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civicplan"))
        config.attributes["connection"] = connection
        command.upgrade(config, "head")


def ready(engine: sa.Engine) -> bool:
    from civicplan.source_schema import metadata
    from civicplan.workflow_schema import metadata as workflow_metadata
    schema = "civicplan" if engine.dialect.name == "postgresql" else None
    with engine.connect() as connection:
        inspector = sa.inspect(connection)
        if not all(inspector.has_table(t.name, schema=schema)
                   for m in (metadata, workflow_metadata) for t in m.tables.values()):
            return False
        return MigrationContext.configure(connection, opts={
            "version_table": "alembic_version_civicplan", "version_table_schema": schema,
        }).get_current_revision() == HEAD
