from alembic import context

from civicplan.source_schema import metadata

connection = context.config.attributes["connection"]
context.configure(
    connection=connection, target_metadata=metadata,
    version_table="alembic_version_civicplan",
    version_table_schema="civicplan" if connection.dialect.name == "postgresql" else None,
)
with context.begin_transaction():
    context.run_migrations()
