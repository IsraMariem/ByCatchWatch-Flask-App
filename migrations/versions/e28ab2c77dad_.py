"""empty message

Revision ID: e28ab2c77dad
Revises: d7e7a9b9c1c5
Create Date: 2024-12-29 23:40:18.805219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e28ab2c77dad'
down_revision = 'd7e7a9b9c1c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('species', schema=None) as batch_op:
        batch_op.add_column(sa.Column('scientific_name', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('common_name', sa.String(length=100), nullable=True))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('species', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
        batch_op.drop_column('common_name')
        batch_op.drop_column('scientific_name')

    # ### end Alembic commands ###
