"""submitted add

Revision ID: 7c7ccadb561c
Revises: 2c76e43373fc
Create Date: 2022-04-12 21:02:09.921817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c7ccadb561c'
down_revision = '2c76e43373fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admission', sa.Column('submitted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admission', 'submitted')
    # ### end Alembic commands ###
