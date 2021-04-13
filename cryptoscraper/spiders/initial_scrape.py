import scrapy


class InitialScrapeSpider(scrapy.Spider):
    name = 'initial_scrape'
    allowed_domains = ['https://www.coingecko.com/en']
    start_urls = ['https://https://www.coingecko.com/en/']

    def parse(self, response):
    	#navigate to respective coins to extract individual coin data
    	coins = response.css('tr td.py-0.coin-name div.center a.d-lg-none.font-bold')
    	yield from response.follow_all(coins, callback=self.get_coin_data)

    	#navigate to the next page
    	next_page = response.css('li.page-item.next a::attr(href)').get()
    	if next_page is not None:
    		yield response.follow(next_page, callback=self.parse)

