import scrapy


class TrendingSpider(scrapy.Spider):
    name = 'trending'
    allowed_domains = ['www.coingecko.com/en']
    start_urls = ['https://www.coingecko.com/en/coins/trending']

    def parse(self, response):
    	data={}
    	for row in response.css('tbody tr'):
        	data['coin_icon'] = row.css('td div.coin-icon span.d-lg-inline.font-normal::text').get()
        	data['coin'] = row.css('td div.center span.d-lg-block.font-bold::text').get()
        	data['volume'] = row.css('td.td-liquidity_score a span::text').get()
        	data['price'] = row.css('td.td-price a span::text').get()
        	data['td-change24h'] = row.css('td.td-change24h span::text').get()

        	yield data


