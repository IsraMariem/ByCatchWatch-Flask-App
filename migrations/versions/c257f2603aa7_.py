"""empty message

Revision ID: c257f2603aa7
Revises: 
Create Date: 2024-12-29 16:51:08.855020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c257f2603aa7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('species',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('scientific_name', sa.String(length=255), nullable=False),
    sa.Column('is_endangered', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bycatch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('port_id', sa.Integer(), nullable=False),
    sa.Column('species_id', sa.Integer(), nullable=False),
    sa.Column('date_caught', sa.DateTime(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['port_id'], ['ports.id'], ),
    sa.ForeignKeyConstraint(['species_id'], ['species.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bycatch_id', sa.Integer(), nullable=False),
    sa.Column('reporter_name', sa.String(length=100), nullable=False),
    sa.Column('contact_info', sa.String(length=255), nullable=False),
    sa.Column('remarks', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['bycatch_id'], ['bycatch.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reports')
    op.drop_table('bycatch')
    op.drop_table('species')
    op.drop_table('ports')
    # ### end Alembic commands ###
