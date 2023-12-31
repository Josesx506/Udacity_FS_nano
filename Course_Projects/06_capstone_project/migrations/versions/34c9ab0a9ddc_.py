"""empty message

Revision ID: 34c9ab0a9ddc
Revises: 11f20d8d364c
Create Date: 2024-01-06 04:58:04.575989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34c9ab0a9ddc'
down_revision = '11f20d8d364c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Bookings', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('Stylists', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Stylists', schema=None) as batch_op:
        batch_op.drop_column('user_id')

    with op.batch_alter_table('Bookings', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###
