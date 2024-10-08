"""Initial migration

Revision ID: d0b4565f6f6a
Revises: 
Create Date: 2024-07-05 20:39:57.620721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0b4565f6f6a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('club',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('profilepicture', sa.String(length=100), nullable=False),
    sa.Column('websitekey', sa.String(length=100), nullable=False),
    sa.Column('shortname', sa.String(length=100), nullable=False),
    sa.Column('summary', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('contact', sa.String(length=100), nullable=True),
    sa.Column('instagram', sa.String(length=100), nullable=True),
    sa.Column('youtube', sa.String(length=100), nullable=True),
    sa.Column('linkedin', sa.String(length=100), nullable=True),
    sa.Column('website', sa.String(length=100), nullable=True),
    sa.Column('facebook', sa.String(length=100), nullable=True),
    sa.Column('twitter', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('club_category_relation',
    sa.Column('clubid', sa.String(length=100), nullable=False),
    sa.Column('categoryname', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('clubid', 'categoryname')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=20), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('officer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('position', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('officer')
    op.drop_table('event')
    op.drop_table('club_category_relation')
    op.drop_table('club')
    # ### end Alembic commands ###
