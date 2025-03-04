"""empty message

Revision ID: ebf105f95329
Revises: 8a3fcd6feb69
Create Date: 2024-12-31 10:36:31.417352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebf105f95329'
down_revision = '8a3fcd6feb69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ports', schema=None) as batch_op:
        batch_op.add_column(sa.Column('region', sa.String(length=100), nullable=True))
        batch_op.drop_column('type')

    with op.batch_alter_table('reports', schema=None) as batch_op:
        batch_op.add_column(sa.Column('species_id', sa.String(), nullable=False))
        batch_op.drop_column('species')

    with op.batch_alter_table('species', schema=None) as batch_op:
        batch_op.add_column(sa.Column('origin', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('species', schema=None) as batch_op:
        batch_op.drop_column('origin')

    with op.batch_alter_table('reports', schema=None) as batch_op:
        batch_op.add_column(sa.Column('species', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.drop_column('species_id')

    with op.batch_alter_table('ports', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.drop_column('region')

    # ### end Alembic commands ###
