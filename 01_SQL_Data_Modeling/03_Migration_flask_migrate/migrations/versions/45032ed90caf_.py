"""empty message

Revision ID: 45032ed90caf
Revises: 
Create Date: 2023-11-15 22:01:44.704472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45032ed90caf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('persons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('persons')
    # ### end Alembic commands ###
