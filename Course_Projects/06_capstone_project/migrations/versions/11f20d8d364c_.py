"""empty message

Revision ID: 11f20d8d364c
Revises: e390cb20e097
Create Date: 2024-01-05 13:29:35.769120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11f20d8d364c'
down_revision = 'e390cb20e097'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Bookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.String(), nullable=True))
        batch_op.drop_column('role')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Bookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
