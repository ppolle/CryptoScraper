from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from cryptoscraper.models import Coin, DailyCoinStats, DailySocialMetrics, DailyGithubMetrics,\
								 Trending, DailyReport, DailyOverallMetrics, db_connect

class Tests:
	def __init__(self):
		engine = db_connect()
		self.Session = sessionmaker(bind=engine)
		self.todays_date = datetime.utcnow().date()
		self.report=""

	def create_report_object(self,session):
		report=session.query(DailyReport).filter_by(date=self.todays_date).first()
		if report is not None:
			return report
		else:
			todays_report=DailyReport(date=self.todays_date)
			try:
				session.add(todays_report)
				session.commit()
			except Exception:
				session.rollback()
				raise

			return todays_report

	def test_daily_coin_stats(self):
		session = self.Session()
		
		todays_coin_stats = session.query(DailyCoinStats.coin_id).filter_by(date=\
			self.todays_date-timedelta(days=1))
		coins = session.query(Coin).filter(Coin.id.notin_(todays_coin_stats)).order_by(Coin.id)
		if coins is not None:
			#update report table
			msg="Daily Coin Stats:\nA total of {} coins were not scrapped. The following are coin details for coins that werent scrapped. Go to the logs for more information about them.\n".format(coins.count())
			for item in coins[:10]:
				msg+="\tCoin:{}, Coin Slug:{}, Coin_id:{}, Coin URL:{}.\n".format(item.name,item.slug,\
					item.id,item.coingecko)
				# print(item.id,item.name,item.slug, item.coingecko)
			self.report+=msg
			print(self.report)
		else:
			pass
			#update report table here
			self.report+="Daily Coin Stats:\n\tDaily coin stats were all successfully crawled."

		print('Coins not scraped are:',coins.count())
		print('Total coins are:',session.query(Coin).count())
		print('Coins scrapped today are:',todays_coin_stats.count())

		session.close()

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
		if trending.count() >= 60:
			daily_report=self.create_report_object(session)
			try:
				daily_report.trending=True
				session.commit()
			except Exception:
				session.rollback()
				raise

			self.report+="Daily Trending:\n\tDaily Trending was succsesfully crawled.\n"
		else:
			daily_report=self.create_report_object(session)
			try:
				daily_report.trending=False
				session.commit()
			except Exception:
				session.rollback()
				raise

			self.report+="Daily Trending:\n\tDaily Trending wasnt succsesfully crawled. Have a look at the logs for more information.\n"

		session.close()

	def test_daily_overall_metrics(self):
		session=self.Session()
		overal_metrics=session.query(DailyOverallMetrics).filter_by(date=self.todays_date).first()
		if overal_metrics is None:
			daily_report=self.create_report_object(session)
			try:
				daily_report.overall_metrics=False
				session.commit()
			except Exception:
				session.rollback()
				raise
			self.report+="Daily Overall Metrics:\nDaily Overall Metrics was not crawled today. Have a look at the logs for more information.\n"
		else:
			daily_report=self.create_report_object(session)
			try:
				daily_report.overall_metrics=True
				session.commit()
			except Exception:
				session.rollback()
				raise
			self.report+="Daily Overall Metrics:\nSuccessfull Crawling and completion of daily overall metrics.\n"

	def test_daily_social_metrics(self):
		session=self.Session()

		todays_social_stats = session.query(DailySocialMetrics.coin_id).filter_by(date=\
			self.todays_date)
		coins = session.query(Coin).filter(Coin.id.notin_(todays_social_stats)).order_by(Coin.id)

		if coins is not None:
			#update report table here
			msg="Daily Social Metrics:\nA total of {} coin social metrics were not crawled. The following are the coin details.".format(coin.count())
			for item in coins:
				msg+="\tCoin:{}, Coin Slug:{}, Coin_id:{}, Coin URL:{}.\n".format(item.name,item.slug,\
					item.id,item.coingecko)

			self.report+=msg
		else:
			#update report table here
			self.report+="Daily Social Metrics:\n\tDaily Social Metrics have all been succesfully crawled."

		session.close()

def main():
	crawl_test=Tests()
	test=crawl_test.test_daily_overall_metrics()

if __name__ == '__main__':
	main()