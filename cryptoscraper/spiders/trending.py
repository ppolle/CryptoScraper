import scrapy
from scrapy.loader import ItemLoader
from cryptoscraper.items import TrendingItem

class TrendingSpider(scrapy.Spider):
    name = 'trending'
    allowed_domains = ['www.coingecko.com/en']
    start_urls = ['https://www.coingecko.com/en/coins/trending']

    def parse(self, response):
    	data = TrendingItem()
    	
    	for row in response.css('tbody tr'):
    		# loader = ItemLoader(item=TrendingItem, response=row)
    		data['coin_slug'] = row.css('td div.coin-icon span.d-lg-inline.font-normal::text').get()
    		data['coin'] = row.css('td div.center span.d-lg-block.font-bold::text').get()
    		data['volume'] = row.css('td.td-liquidity_score a span::text').get()
    		data['price'] = row.css('td.td-price a span::text').get()
    		data['change24h'] = row.css('td.td-change24h span::text').get()

    		#assign values to loader
    		# loader.add_value('coin', data['coin'])
    		# loader.add_value('coin_slug', data['coin_icon'])
    		# loader.add_value('volume', data['volume'])
    		# loader.add_value('price', data['price'])
    		# loader.add_value('change24h', data['change24h'])

    	yield data



