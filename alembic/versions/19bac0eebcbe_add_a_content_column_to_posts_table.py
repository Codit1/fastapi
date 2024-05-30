"""add a content column to posts table

Revision ID: 19bac0eebcbe
Revises: 46d528976d55
Create Date: 2024-05-28 20:52:46.137660

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19bac0eebcbe'
down_revision: Union[str, None] = '46d528976d55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
