"""followers

Revision ID: 46b8eb2ea8d1
Revises: 9e78aa30ac79
Create Date: 2019-08-05 10:56:58.129622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46b8eb2ea8d1'
down_revision = '9e78aa30ac79'
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
