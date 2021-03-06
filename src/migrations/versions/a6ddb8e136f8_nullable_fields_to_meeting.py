"""nullable fields to Meeting

Revision ID: a6ddb8e136f8
Revises: 86cd34fa749f
Create Date: 2021-07-09 17:31:11.047069

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a6ddb8e136f8'
down_revision = '86cd34fa749f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('meeting', 'welcome_message',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('meeting', 'moderator_message',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('meeting', 'moderator_message',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('meeting', 'welcome_message',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###
