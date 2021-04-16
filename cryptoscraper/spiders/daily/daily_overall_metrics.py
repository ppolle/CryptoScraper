import scrapy
from scrapy.loader import ItemLoader
from cryptoscraper.items import DailyOverallMetricsItem

class DailyOverallMetricsSpider(scrapy.Spider):
    name = 'daily_overall_metrics'
    start_urls = ['https://www.coingecko.com/en/overall_stats']

    def parse(self, response):
        data = DailyOverallMetricsItem()
        for item in response.css('div.mr-3'):
            if item.css('span.font-bold::text').get() == 'Coins':
                data['coins'] = item.css('a.cyan-color::text').get()
            
            if item.css('span.font-bold::text').get() == 'Exchanges':
                data['exchanges'] = item.css('a.cyan-color::text').get()

            if item.css('span.font-bold::text').get() == 'Market Cap':
                data['market_cap'] = "{} {}".format(item.css('a span.cyan-color::text').get(), item.css('span.text-green::text').get())
            
            if item.css('span.font-bold::text').get() == '24h Vol':
                data['twenty_four_vol'] = item.css('span.cyan-color::text').get()

        data['dominance'] = response.css('div.mr-2::text').getall()
        data['eth_gas'] = response.css('div.ml-2.mr-1::text')[1].get()

        yield data

