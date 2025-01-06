"""empty message

Revision ID: 1213f99156c5
Revises: 5238d7a5c6d3
Create Date: 2025-01-06 15:42:32.870233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1213f99156c5'
down_revision = '5238d7a5c6d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('background', sa.Enum('RESEARCHER', 'FISHERMAN', 'NGO', 'BYCATCH_ACTIVIST', 'OBSERVER', name='userbackground'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('background')

    # ### end Alembic commands ###
