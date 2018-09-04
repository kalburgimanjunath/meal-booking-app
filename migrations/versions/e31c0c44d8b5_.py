"""empty message

Revision ID: e31c0c44d8b5
Revises: d108e936c61b
Create Date: 2018-09-03 15:21:52.714912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e31c0c44d8b5'
down_revision = 'd108e936c61b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menus', sa.Column('day', sa.String(length=20), nullable=True))
    op.drop_column('menus', 'date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menus', sa.Column('date', sa.DATE(), autoincrement=False, nullable=True))
    op.drop_column('menus', 'day')
    # ### end Alembic commands ###
