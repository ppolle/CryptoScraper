"""update circulating supply fields

Revision ID: 7b47998b707e
Revises: e5837d215cca
Create Date: 2021-05-15 00:12:20.052286

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from cryptoscraper.models import DailyCoinStats
from cryptoscraper.utils import get_num


# revision identifiers, used by Alembic.
revision = '7b47998b707e'
down_revision = 'e5837d215cca'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    stats = session.query(DailyCoinStats).all()
    for item in session.query(DailyCoinStats).yield_per(5000):
      circulating_supply = item.circulating_supply
      if circulating_supply is not None and '/' in circulating_supply:
        split_circ = circulating_supply.split('/')
        circ= get_num(split_circ[0])
        max_supply = get_num(split_circ[1])
        item.circulating_supply = circ
        if item.max_supply is None or item.max_supply==0:
          item.max_supply = max_supply

    session.commit()


def downgrade():
    pass
