"""empty message

Revision ID: b4e88ee4e3ac
Revises: 34c9ab0a9ddc
Create Date: 2024-01-06 05:01:53.571459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4e88ee4e3ac'
down_revision = '34c9ab0a9ddc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Stylists', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Stylists', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###
