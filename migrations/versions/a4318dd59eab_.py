"""empty message

Revision ID: a4318dd59eab
Revises: 05d75fbdf0c2
Create Date: 2018-11-26 14:50:45.873736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4318dd59eab'
down_revision = '05d75fbdf0c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cms_banner',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=False),
    sa.Column('link_url', sa.String(length=255), nullable=False),
    sa.Column('weight_url', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cms_banner')
    # ### end Alembic commands ###
