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
    'daily-scraper': {
        'task': 'tasks.daily_scraper',
        'schedule': crontab(minute=0, hour=3),
    },
    'monthly-scraper':{
	    'task': 'tasks.monthly_scraper',
	    'schedule': crontab(0,0,day_of_month='1'),
    },
    'initial-scrape':{
        'task': 'tasks.initial_scraper',
        'schedule': crontab(minute=40, hour=14,day_of_month='25'),
    },
    'test-scrape':{
    'task': 'tasks.testing_Scraper',
    'schedule': crontab(minute='*/3'),
    }
}

app.conf.timezone = 'UTC'

@app.task
def initial_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(InitialScrapeSpider)
    process.start()

@app.task    
def daily_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(coin_stats.DailyCoinStatsSpider)
    process.crawl(trending.TrendingSpider)
    process.crawl(daily_overall_metrics.DailyOverallMetricsSpider)
    process.crawl(github_stats.GithubStatsSpider)
    process.start()

@app.task
def monthly_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ProjectScoreSpider)
    process.start()

@app.task
def testing_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(trending.TrendingSpider)
    process.start()
