"""email and phone number

Revision ID: 8401545ef1e0
Revises: 22f9cf4077bf
Create Date: 2024-08-23 20:56:44.243018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8401545ef1e0'
down_revision = '22f9cf4077bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('club', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=300), nullable=True))
        batch_op.add_column(sa.Column('phonenumber', sa.String(length=300), nullable=True))

    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.alter_column('club_value',
               existing_type=sa.FLOAT(),
               nullable=False)
        batch_op.alter_column('member_count',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.alter_column('member_count',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('club_value',
               existing_type=sa.FLOAT(),
               nullable=True)

    with op.batch_alter_table('club', schema=None) as batch_op:
        batch_op.drop_column('phonenumber')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
