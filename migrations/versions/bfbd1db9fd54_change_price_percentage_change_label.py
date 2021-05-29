"""change price percentage change label

Revision ID: bfbd1db9fd54
Revises: 507d6aff9683
Create Date: 2021-05-21 10:59:11.654096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfbd1db9fd54'
down_revision = '507d6aff9683'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('daily_coin_stats', 'price_percentage_change',new_column_name='usd_percentage_change')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('daily_coin_stats', 'usd_percentage_change', new_column_name='price_percentage_change')
    # ### end Alembic commands ###