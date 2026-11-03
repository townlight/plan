from alembic import context

from townlight_planning.source_schema import metadata

connection = context.config.attributes["connection"]
context.configure(
    connection=connection, target_metadata=metadata,
    version_table="alembic_version_townlight_planning",
    version_table_schema="townlight_planning" if connection.dialect.name == "postgresql" else None,
)
with context.begin_transaction():
    context.run_migrations()
