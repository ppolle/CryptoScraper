import scrapy


class DailyOverallMetricsSpider(scrapy.Spider):
    name = 'daily_overall_metrics'
    allowed_domains = ['https://www.coingecko.com/en']
    start_urls = ['https://www.coingecko.com/en/overall_stats']

    def parse(self, response):
    	for item in response.css('div.mr-3'):
    		if item.css('span.font-bold::text').get() == 'Coins':
    			coins = item.css('a.cyan-color::text').get()

    		if item.css('span.font-bold::text').get() == 'Exchanges':
    			exchanges = item.css('a.cyan-color::text').get()

    		if item.css('span.font-bold::text').get() == 'Market Cap':
    			market_cap = "{} {}".format(item.css('span.cyan-color::text').get(), item.css('span.text-green::text').get())

    		# if item.css('span.font-bold::text').get() == '24h Vol':
    		# 	twenty_four_vol = item.css('span.cyan-color::text').get() + item.css('span.text-green::text').get()

    	dominance = response.css('div.mr-2::text').getall()
    	eth_gas = response.css('div.ml-2.mr-1::text').get()

    	yield{
    	'Coins': coins,
    	'Exchanges': exchanges,
    	'Market cap': market_cap,
    	# '24h Vol': twenty_four_vol,
    	'Dominance': dominance,
    	'ETH Gas': eth_gas
    	}

