from datetime import datetime
from sqlalchemy.orm import sessionmaker
from ..cryptoscraper.models import Coin, DailyCoinStats, DailyGithubMetrics, Trending, db_connect

class Tests:
	def __init__(self):
		engine = db_connect()
		self.Session = sessionmaker(bind=engine)
		self.todays_date = datetime.utcnow().date()

	def test_daily_coin_stats(self):
		session = self.Session()
		
		todays_coin_stats = session.query(DailyCoinStats.id).filter_by(date=self.todays_date)
		coins = session.query(Coin).filter(Coin.id.notin_(todays_coin_stats))
		if coins is not None:
			print(len(coins))
			print(coins.count())
			print('This is working')
		

		session.close()
		pass

	def test_daily_github_metrics(self):
		yesterdays_date=self.todays_date-1
		yesterdays_metrics=session.query(DailyGithubMetrics).filter_by(date=yesterdays_date)
		todays_metrics=session.query(DailyGithubMetrics).filter_by(date=self.todays_date)
		if len(todays_metrics) < len(yesterdays_metrics):
			print('Ni kunoma brather')
			#find a way of finding the repositories that were not scrapped
		pass

	def test_trending(self):
		session=self.Session()
		trending = session.query(Trending).filter_by(date=self.todays_date)
		if len(trending) >= 60:
			print('Everythings good')

		session.close()

	def test_daily_overall_metrics(self):
		session=self.Session()
		overal_metrics=session.query(DailyOverallMetrics).filter_by(date=self.todays_date)
		if overal_metrics is not None:
			pass

	def test_daily_socail_metrics(self):
		pass


def main():
	crawl_test=Tests()
	test=crawl_test.test_daily_coin_stats()

if __name__ == '__main__':
	main()