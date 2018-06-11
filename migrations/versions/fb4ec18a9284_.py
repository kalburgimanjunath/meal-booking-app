"""empty message

Revision ID: fb4ec18a9284
Revises: 868a051cc263
Create Date: 2018-06-11 02:29:56.436639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb4ec18a9284'
down_revision = '868a051cc263'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menus', sa.Column('image_url', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('menus', 'image_url')
    # ### end Alembic commands ###
