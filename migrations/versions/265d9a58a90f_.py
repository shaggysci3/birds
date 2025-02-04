"""empty message

Revision ID: 265d9a58a90f
Revises: 9135d5698576
Create Date: 2025-01-22 20:51:28.808534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '265d9a58a90f'
down_revision = '9135d5698576'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('album_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(batch_op.f('fk_songs_album_id_featuredAlbum'), 'featuredAlbum', ['album_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_songs_album_id_featuredAlbum'), type_='foreignkey')
        batch_op.drop_column('album_id')

    # ### end Alembic commands ###
