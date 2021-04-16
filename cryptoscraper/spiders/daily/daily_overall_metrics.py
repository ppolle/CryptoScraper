import scrapy
from scrapy.loader import ItemLoader
from cryptoscraper.items import DailyOverallMetricsItem

class DailyOverallMetricsSpider(scrapy.Spider):
    name = 'daily_overall_metrics'
    start_urls = ['https://www.coingecko.com/en/overall_stats']

    def parse(self, response):
    	for item in response.css('div.mr-3'):
    		if item.css('span.font-bold::text').get() == 'Coins':
    			coins = item.css('a.cyan-color::text').get()

    		if item.css('span.font-bold::text').get() == 'Exchanges':
    			exchanges = item.css('a.cyan-color::text').get()

    		if item.css('span.font-bold::text').get() == 'Market Cap':
    			market_cap = "{} {}".format(item.css('a span.cyan-color::text').get(), item.css('span.text-green::text').get())

    		if item.css('span.font-bold::text').get() == '24h Vol':
    			twenty_four_vol = item.css('span.cyan-color::text').get()

    	dominance = response.css('div.mr-2::text').getall()
    	eth_gas = response.css('div.ml-2.mr-1::text')[1].get()

        loader = ItemLoader(item=DailyOverallMetricsItem)
        
        loader.add_value('coins', coins)
        loader.add_value('exchanges', exchanges)
        loader.add_value('market_cap', market_cap)
        loader.add_value('twenty_four_vol', twenty_four_vol)
        loader.add_value('dominance', dominance)
        loader.add_value('eth_gas', eth_gas)


    	# yield{
    	# 'Coins': coins,
    	# 'Exchanges': exchanges,
    	# 'Market cap': market_cap,
    	# '24h Vol': twenty_four_vol,
    	# 'Dominance': dominance,
    	# 'ETH Gas': eth_gas
    	# }

        yield loader.load_item()

