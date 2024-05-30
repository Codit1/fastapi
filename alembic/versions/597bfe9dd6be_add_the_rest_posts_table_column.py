"""add the rest posts table column

Revision ID: 597bfe9dd6be
Revises: 7292d6f7f448
Create Date: 2024-05-28 22:46:26.289442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '597bfe9dd6be'
down_revision: Union[str, None] = '7292d6f7f448'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False))
    op.add_column("posts",sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))
    pass


def downgrade():
    op.drop_column("posts, published")
    op.drop_column("posts", "created_at")
    pass
