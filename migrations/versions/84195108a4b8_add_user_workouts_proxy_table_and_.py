"""add user_workouts proxy table and relationships between workouts and users I am commiting this 6 hours after I did it I hope I was done

Revision ID: 84195108a4b8
Revises: b90d3ede45c2
Create Date: 2024-06-28 01:15:30.144640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84195108a4b8'
down_revision = 'b90d3ede45c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_workouts',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_workouts_user_id_users')),
    sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], name=op.f('fk_user_workouts_workout_id_workouts')),
    sa.PrimaryKeyConstraint('user_id', 'workout_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_workouts')
    # ### end Alembic commands ###