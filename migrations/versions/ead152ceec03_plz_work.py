"""plz work

Revision ID: ead152ceec03
Revises: fa91ba96cdb2
Create Date: 2024-06-26 19:23:15.118755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ead152ceec03'
down_revision = 'fa91ba96cdb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workouts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('timer', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('workoutss')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workoutss',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('img', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('timer', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='workoutss_pkey')
    )
    op.drop_table('workouts')
    # ### end Alembic commands ###
