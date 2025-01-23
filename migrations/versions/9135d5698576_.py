"""empty message

Revision ID: 9135d5698576
Revises: 82161c8c4d9d
Create Date: 2025-01-22 20:33:04.797327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9135d5698576'
down_revision = '82161c8c4d9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('featuredAlbum',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('songs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('song', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('songs')
    op.drop_table('featuredAlbum')
    # ### end Alembic commands ###
