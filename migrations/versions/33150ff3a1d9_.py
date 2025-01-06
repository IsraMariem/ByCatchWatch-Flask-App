"""empty message

Revision ID: 33150ff3a1d9
Revises: c257f2603aa7
Create Date: 2024-12-29 21:04:07.430336
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '33150ff3a1d9'
down_revision = 'c257f2603aa7'
branch_labels = None
depends_on = None


def upgrade():
    # Since the changes have already been applied to the database, no changes are necessary here.
    pass


def downgrade():
    # Since the changes have already been applied to the database, no need to undo them.
    pass



