"""followers

Revision ID: 799be54035c5
Revises: 255c11c06556
Create Date: 2020-12-31 10:49:21.924401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '799be54035c5'
down_revision = '255c11c06556'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
