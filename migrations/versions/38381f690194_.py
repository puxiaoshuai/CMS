"""empty message

Revision ID: 38381f690194
Revises: a4318dd59eab
Create Date: 2018-11-26 15:48:03.615145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38381f690194'
down_revision = 'a4318dd59eab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_banner', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cms_banner', 'create_time')
    # ### end Alembic commands ###