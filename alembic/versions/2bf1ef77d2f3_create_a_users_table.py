"""create a users table

Revision ID: 2bf1ef77d2f3
Revises: 19bac0eebcbe
Create Date: 2024-05-28 21:09:58.251879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bf1ef77d2f3'
down_revision: Union[str, None] = '19bac0eebcbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("users", sa.Column("id",sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone='True'), nullable=False, server_default=sa.text('NOW()')),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"))
    pass


def downgrade():
    op.drop_table("users")
    pass
