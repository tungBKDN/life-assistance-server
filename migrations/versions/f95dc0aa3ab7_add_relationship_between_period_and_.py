"""Add relationship between Period and Schedule

Revision ID: f95dc0aa3ab7
Revises: b35bd025acbf
Create Date: 2024-12-07 01:05:14.848553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f95dc0aa3ab7'
down_revision = 'b35bd025acbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('period', schema=None) as batch_op:
        batch_op.alter_column('drug_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('period', schema=None) as batch_op:
        batch_op.alter_column('drug_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)

    # ### end Alembic commands ###
