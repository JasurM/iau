"""Is accepted

Revision ID: 2c76e43373fc
Revises: 2adf75c346d6
Create Date: 2022-04-12 19:09:01.598221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c76e43373fc'
down_revision = '2adf75c346d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admission', sa.Column('accepted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admission', 'accepted')
    # ### end Alembic commands ###
