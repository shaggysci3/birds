"""create table birds

Revision ID: 528f78f67cd0
Revises: 
Create Date: 2024-06-22 22:44:36.363812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '528f78f67cd0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('birds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('species', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('birds')
    # ### end Alembic commands ###
