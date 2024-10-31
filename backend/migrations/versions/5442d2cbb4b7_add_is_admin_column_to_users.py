"""add_is_admin_column_to_users

Revision ID: 5442d2cbb4b7
Revises: e0f373926ab4
Create Date: 2024-10-11 13:17:11.057702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5442d2cbb4b7'
down_revision: Union[str, None] = 'e0f373926ab4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the is_admin column to the users table
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), default=False, nullable=False))
    
def downgrade():
    # Remove the is_admin column if downgrading
    op.drop_column('users', 'is_admin')