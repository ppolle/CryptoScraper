from datetime import datetime
from sqlalchemy.orm import sessionmaker
from cryptoscraper.models import Coin, DailyCoinStats,  db_connect

class Tests:
	def __init__(self):
		engine = db_connect()
		self.Session = sessionmaker(bind=engine)
		self.todays_date = datetime.utcnow().date()

	def test_daily_coin_stats(self):
		session = self.Session()
		
		coins = session.query(Coin).order_by(Coin.id).all()
		todays_coin_stats = session.query(DailyCoinStats).filter_by(date=self.todays_date).all()

