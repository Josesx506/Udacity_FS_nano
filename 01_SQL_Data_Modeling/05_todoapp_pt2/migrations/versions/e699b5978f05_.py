"""empty message

Revision ID: e699b5978f05
Revises: 5ec33d95ee89
Create Date: 2023-11-20 20:44:13.055746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e699b5978f05'
down_revision = '5ec33d95ee89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.alter_column('list_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.alter_column('list_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###