import scrapy
from scrapy.loader import ItemLoader
from cryptoscraper.items import DailyOverallMetricsItem
from cryptoscraper.utils import get_slug, get_name, get_num, sanitize_string

class DailyOverallMetricsSpider(scrapy.Spider):
    name = 'daily_overall_metrics'
    start_urls = ['https://www.coingecko.com/en/overall_stats']

    def parse(self, response):
        data = DailyOverallMetricsItem()
        for item in response.css('div.mr-3'):
            if item.css('span.font-bold::text').get() == 'Coins':
                data['coins'] = get_num(item.css('a.cyan-color::text').get())
            
            if item.css('span.font-bold::text').get() == 'Exchanges':
                data['exchanges'] = get_num(item.css('a.cyan-color::text').get())

            if item.css('span.font-bold::text').get() == 'Market Cap':
                data['market_cap'] = get_num(item.css('a span.cyan-color::text').get())
            
            if item.css('span.font-bold::text').get() == '24h Vol':
                data['twenty_four_vol'] = get_num(item.css('span.cyan-color::text').get())

        data['dominance'] = sanitize_string(response.css('div.mr-2::text').getall())
        data['eth_gas'] = sanitize_string(response.css('div.ml-2.mr-1::text')[1].get())

        yield data

