# SPDX-License-Identifier: AGPL-3.0-only
"""Explicit imported policy neighborhood applicability; preserve source history."""
from alembic import op
import sqlalchemy as sa

revision = "civicplan_0004"
down_revision = "civicplan_0003"


def upgrade():
    connection = op.get_bind()
    schema = "civicplan" if connection.dialect.name == "postgresql" else None
    columns = sa.inspect(connection).get_columns("source_policies", schema=schema)
    if not any(column["name"] == "neighborhoods" for column in columns):
        op.add_column("source_policies", sa.Column("neighborhoods", sa.JSON,
                      nullable=False, server_default=sa.text("'[]'")), schema=schema)


def downgrade():
    raise RuntimeError("Neighborhood applicability is retained source evidence; restore a verified backup")
