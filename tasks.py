from celery import Celery
from celery.schedules import crontab
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from cryptoscraper.spiders.initial.initial_scrape import InitialScrapeSpider
from cryptoscraper.spider.daily import coin_stats, daily_overall_metrics, github_stats

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
}

app.conf.timezone = 'UTC'

@app.task
def add(x, y):
    return x + y

@app.task    
def daily_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(InitialScrapeSpider)
    process.start()
    pass

@app.task
def monthly_scraper():
	pass

@app.task
def trending_scraper():
	pass