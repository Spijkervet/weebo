"""empty message

Revision ID: 7202f7c152ff
Revises: 0ed01bfe41c0
Create Date: 2017-08-19 12:46:59.135014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7202f7c152ff'
down_revision = '0ed01bfe41c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
