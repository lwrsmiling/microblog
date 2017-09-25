"""empty message

Revision ID: 814dd52642e1
Revises: 0148af141cc2
Create Date: 2017-08-12 20:22:55.295477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '814dd52642e1'
down_revision = '0148af141cc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    # ### end Alembic commands ###
