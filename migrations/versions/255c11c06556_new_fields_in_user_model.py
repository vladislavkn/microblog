"""new fields in user model

Revision ID: 255c11c06556
Revises: 77873639e598
Create Date: 2020-12-30 20:38:51.000021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '255c11c06556'
down_revision = '77873639e598'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=192), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
