"""Use ProjectStatusEnum from schemas

Revision ID: 1fdc71445563
Revises: 2c9537f61aec
Create Date: 2024-10-15 17:24:51.307977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1fdc71445563'
down_revision: Union[str, None] = '2c9537f61aec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Execute the raw SQL to alter the column type and provide the conversion
    op.execute("ALTER TABLE projects ALTER COLUMN status TYPE projectstatusenum USING status::text::projectstatusenum;") 


def downgrade():
    # For downgrading, you might need to handle the enum type conversion carefully
    # depending on how you want to revert the changes
    op.execute("ALTER TABLE projects ALTER COLUMN status TYPE projectstatus USING status::text::projectstatus;")
