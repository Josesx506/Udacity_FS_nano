"""empty message

Revision ID: 8d102bbe7842
Revises: c3de70299ec2
Create Date: 2024-01-06 16:41:41.719094

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8d102bbe7842'
down_revision = 'c3de70299ec2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Stylists', schema=None) as batch_op:
        batch_op.drop_column('skills')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Stylists', schema=None) as batch_op:
        batch_op.add_column(sa.Column('skills', postgresql.ARRAY(sa.VARCHAR(length=120)), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
