# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pytz
from datetime import datetime
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from cryptoscraper.models import DailyOverallMetrics, DailyGithubMetrics, DailyCoinStats, Coin,\
                                    Trending, HistoricalData, ProjectScore, DailySocialMetrics, db_connect, create_table

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
        self.todays_date = datetime.utcnow().date()

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
            	except Exception:
            		session.rollback()
            		raise
            	finally:
            		session.close()

            return item
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
            coin.contract = item['contract']

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

            # existing_historical_entry = session.query(HistoricalData).filter_by(date=historical_data.date).first()
            # if existing_historical_entry is not None:
            #     print(existing_historical_entry)
            #     raise DropItem("Duplicate entry for today was found")
            #     session.close()
            # else:
            try:
                session.add(historical_data)
                session.commit()
            except Exception:
                session.rollback()
                raise

            finally:
                session.close()

            return item

        return item

class ProjectScorePipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.todays_date = datetime.utcnow().date()

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
                project_score.coin = coin

                try:
                    session.add(project_score)
                    session.commit()

                except Exception:
                    session.rollback()
                    raise

                finally:
                    session.close()

            return item
        return item

class TrendingPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.todays_date = datetime.utcnow().date()

    def process_item(self, item, spider):
        if spider.name == 'trending':
            session = self.Session()
            trending = Trending()

            trending.slug = item['coin_slug']
            trending.volume = item['volume']
            trending.price = item['price']
            trending.percentage_change = item['change24h']
            trending.coin = item['coin']
            trending.date = self.todays_date

            try:
                session.add(trending)
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

            return item

        return item

class GithubMetricsPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.todays_date = datetime.utcnow().date()

    def process_item(self, item, spider):
        if spider.name == 'github_stats':
            session =self.Session()
            github = DailyGithubMetrics()

            github.date=self.todays_date
            github.repo_name = item['repo_name']
            github.url = item['url']
            github.stars = item['stars']
            github.watchers = item['watchers']
            github.forks = item['forks']
            github.contributors =item['contributors']
            github.merged_pr =item['merged_pr']
            github.closed_total_issue = item['issues']

            coin = session.query(Coin).filter_by(data_coin_id=item['data_coin_id']).first()

            if coin is None:
                raise DropItem("This coin is currently not available. Please run the initial scraper to have it in the database first")
            else:
                github.coin = coin

                try:
                    session.add(github)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    raise
                finally:
                    session.close()

            return item
        return item

class DailyCoinScrapePipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.todays_date = datetime.utcnow().date()

    def process_item(self, item, spider):
        if spider.name == 'coin_stats':
            session = self.Session()
            coin = Coin()
            coin_stats = DailyCoinStats()
            social = DailySocialMetrics()

            coin.name = item['name']
            coin.slug = item['slug']
            coin.website = item['website']
            coin.coingecko = item['coingecko']
            coin.community = item['community']
            coin.tags = item['tags']
            coin.data_coin_id = item['data_coin_id']
            coin.contract = item['contract']

            social.redit_subscribers = item['redit_subscribers']
            social.active_redit_ac = item['active_redit_ac']
            social.avg_posts_per_hr = item['avg_posts_per_hr']
            social.avg_comments_per_hr = item['avg_comments_per_hr']
            social.twitter_followers = item['twitter_followers']
            social.telegram_users = item['telegram_users']
            social.date = self.todays_date

            coin_stats.price = item['coin_price']
            coin_stats.date = self.todays_date
            coin_stats.percentage_change = item['percentage_change']
            coin_stats.likes = item['likes']
            coin_stats.circulating_supply = item['circulating_supply']
            coin_stats.fully_diluted_valuation = item['fully_diluted_valuation']
            coin_stats.max_supply = item['max_supply']
            coin_stats.market_cap = item['market_cap']
            coin_stats.market_cap_dominance = item['market_cap_dominance']
            coin_stats.coin_roi = item['coin_roi']
            coin_stats.volume_market_cap = item['volume_market_cap']
            coin_stats.trading_volume = item['volume_market_cap']
            coin_stats.daily_low_high = item['daily_low_high']
            coin_stats.weekly_low_high = item['weekly_low_high']
            coin_stats.market_cap_rank = item['market_cap_rank']
            coin_stats.all_time_high = item['all_time_high']
            coin_stats.all_time_high_date = item['all_time_high_date']
            coin_stats.all_time_low = item['all_time_low']
            coin_stats.all_time_low_date = item['all_time_low_date']

            existing_coin = session.query(Coin).filter_by(data_coin_id = coin.data_coin_id).first()

            if existing_coin:
                social.coin = existing_coin
                coin_stats.coin = existing_coin
            else:
                social.coin = coin
                coin_stats.coin = coin

            try:
                # if existing_coin:
                #     session.add(coin)
                # session.add(coin_stats)
                session.add(social)

                session.commit()
            except Exception:
                session.rollback()
                raise

            finally:
                session.close()

            return item

        return item

class DuplicatesPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.todays_date = datetime.utcnow().date()

    def process_item(self, item, spider):

        if spider.name == 'coin_stats':
            session = self.Session()
            coin = session.query(Coin).filter_by(data_coin_id=item['data_coin_id']).first()
            if coin is not None:
                existing_coin_stats = session.query(DailyCoinStats).filter_by(coin_id=coin.id,date=self.todays_date).first()
                if existing_coin_stats is not None:
                    raise DropItem("Dropping daily coin stats item because it already exists")
                else:
                    return item
            else:
                return item
        elif spider.name == 'github_stats':
            session = self.Session()
            coin = session.query(Coin).filter_by(data_coin_id=item['data_coin_id']).first()
            git_exist = session.query(DailyGithubMetrics).filter_by(repo_name=item['repo_name'], date=self.todays_date, coin_id=coin.id).first()
            session.close()
            if git_exist is not None:
                raise DropItem('Droping item because it already exists')
            else:
                return item
        elif spider.name == 'trending':
            session = self.Session()
            existing_trend = session.query(Trending).filter_by(coin=item['coin'],slug=item['coin_slug'],date=self.todays_date).first()
            session.close()
            if existing_trend is not None:
                raise DropItem('This trend already exists for today')
            else:
                return item
        elif spider.name == 'project_score':
            return item
        elif spider.name == 'initial_scrape':
            session = self.Session()
            coin = session.query(Coin).filter_by(data_coin_id=item['data_coin_id']).first()
            session.close()
            if coin is not None:
                session = self.Session()
                existing_history = session.query(HistoricalData).filter_by(coin_id=coin.id,date=item['date']).first()
                session.close()

                if existing_history is not None:
                    raise DropItem('This history entry for {},on {} was already created'.format(coin.name, item['date'].strftime('%d, %b %Y')))
                else:
                    return item
            else:
                return item
        elif spider.name == 'daily_overall_metrics':
            return item
        else:
            return item
