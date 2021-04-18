# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import date
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from cryptoscraper.models import DailyOverallMetrics, Coin, HistoricalData, ProjectScore, db_connect, create_table

class CryptoscraperPipeline:
    def process_item(self, item, spider):
        return item

class DailyOverallMetricsPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.todays_date = date.today()

    def process_item(self, item, spider):
        if spider.name == "daily_overall_metrics":
            session = self.Session()
            daily_metrics = DailyOverallMetrics()
            
            daily_metrics.coins = item['coins']
            daily_metrics.exchanges = item['exchanges']
            daily_metrics.market_cap = item['market_cap']
            daily_metrics.daily_vol = item['twenty_four_vol']
            daily_metrics.dominance = item['dominance']
            daily_metrics.eth_gas = item['eth_gas']
            daily_metrics.date = self.todays_date

            if session.query(DailyOverallMetrics).filter_by(date = daily_metrics.date).first():
                raise DropItem("Duplicate entry for today was found")
                session.close()
            else:
            	try:
            		session.add(daily_metrics)
            		session.commit()
            	except:
            		session.rollback()
            		raise
            	finally:
            		session.close()

            	return item

class InitialScrapePipeline:
    def __init__(self):
        """
        Initializes database connection adn sessionmaker
        Create tables
        """

        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if spider.name == 'initial_scrape':
            session = self.Session()
            coin = Coin()
            historical_data = HistoricalData()

            coin.name = item['name']
            coin.slug = item['slug']
            coin.website = item['website']
            coin.coingecko = item['coingecko']
            coin.community = item['community']
            coin.tags = item['tags']
            coin.data_coin_id = item['data_coin_id']

            historical_data.date = item['date']
            historical_data.market_cap =item['market_cap']
            historical_data.volume = item['volume']
            historical_data.market_open = item['market_open']
            historical_data.market_close = item['market_close']

            existing_coin = session.query(Coin).filter_by(data_coin_id = coin.data_coin_id).first()

            if existing_coin is not None:
                historical_data.coin = existing_coin
                # existing_historical_entry = session.query(HistoricalData).filter_by(date=historical_data.date, coin=existing_coin).first()
            else:
                historical_data.coin = coin
                # existing_historical_entry = session.query(HistoricalData).filter_by(date=historical_data.date, coin=coin).first()

            existing_historical_entry = session.query(HistoricalData).filter_by(date=historical_data.date).first()
            if existing_historical_entry is not None:
                print(existing_historical_entry)
                raise DropItem("Duplicate entry for today was found")
                session.close()
            else:
                try:
                    session.add(historical_data)
                    session.commit()
                except:
                    session.rollback()

                finally:
                    session.close()

                return item

class ProjectScorePipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.todays_date = date.today()

    def process_item(self, item, spider):
        if spider.name == 'project_score':
            session = self.Session()
            project_score = ProjectScore()

            project_score.date = self.todays_date
            project_score.team_score = item['team_score']
            project_score.eco_sys_score = item['eco_score']
            project_score.project_score = item['project_score']
            project_score.outlook = item['outlook']
            project_score.insight = item['insight']

            coin = session.query(Coin).filter_by(data_coin_id=item['data_coin_id']).first()

            if coin is None:
                raise DropItem("This coin doesnt exist in the DB")
            else:
                project_score.coin = coin.id

                try:
                    session.add(project_score)
                    session.commit()

                except:
                    session.rollback()

                finally:
                    session.close()

            return item

