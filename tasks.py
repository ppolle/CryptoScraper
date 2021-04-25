from celery import Celery
from celery.schedules import crontab

from cryptoscraper.spiders.initial.initial_scrape import InitialScrapeSpider
from cryptoscraper.spiders.monthly.project_score import ProjectScoreSpider
from cryptoscraper.spiders.daily import coin_stats, daily_overall_metrics, github_stats, trending

from billiard.context import Process
from scrapy.crawler import Crawler
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

app = Celery('tasks', broker='pyamqp://guest@localhost//')

app.conf.beat_schedule = {
    # 'daily-scraper': {
    #     'task': 'tasks.daily_scraper',
    #     'schedule': crontab(minute=0, hour=3),
    # },
    'monthly-scraper':{
	    'task': 'tasks.monthly_scraper',
	    # 'schedule': crontab(0,0,day_of_month='1'),
        'schedule': crontab(minute='*/3')
    },
    # 'initial-scrape':{
    #     'task': 'tasks.initial_scraper',
    #     'schedule': crontab(minute=40, hour=14,day_of_month='25'),
    # },
}

app.conf.timezone = 'UTC'

class CrawlerProcess(Process):
    def __init__(self, spider):
        Process.__init__(self)
        settings = get_project_settings()
        self.crawler = Crawler(spider.__class__, settings)
        self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        self.spider = spider

    def run(self):
        self.crawler.crawl(self.spider)
        reactor.run()

@app.task
def initial_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(InitialScrapeSpider)
    process.start()

@app.task    
def daily_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(coin_stats.DailyCoinStatsSpider)
    process.crawl(daily_overall_metrics.DailyOverallMetricsSpider)
    process.crawl(github_stats.GithubStatsSpider)
    process.crawl(trending.TrendingSpider)
    process.start()

@app.task
def monthly_scraper():
    crawler = CrawlerProcess(trending.TrendingSpider)
    crawler.start()
    crawler.join()
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    # runner = CrawlerRunner()
    # d = runner.crawl(trending.TrendingSpider)
    # d.addBoth(lambda _: reactor.stop())

    # for crawler in runner.crawlers:
    #     crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    # reactor.run()


    # process = CrawlerProcess(get_project_settings())
    # # process.crawl(ProjectScoreSpider)
    # process.crawl(trending.TrendingSpider)
    # process.start()
