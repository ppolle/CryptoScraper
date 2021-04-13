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

    def get_coin_data(self, response):

    	links = response.css('div.coin-link-row.mb-md-0')
    	for link in links:
    		if link.css('span.coin-link-title.mr-2::text').get() == 'Website':
    			websites = link.css('a.coin-link-tag::attr(href)').getall()

    		if link.css('span.coin-link-title.mr-2::text').get() == 'Tags':
    			tags = link.css('a.coin-link-tag::attr(href)').getall() + link.css('span.coin-tag.mr-1::text').getall()

    		if link.css('span.coin-link-title.mr-2::text').get() == 'Community':
    			community = link.css('a.coin-link-tag::attr(href)').getall()

    	yield {
    	'Name': response.css('h1.mr-md-3.mx-2.mb-md-0.text-3xl.font-semibold::text').get(),
    	'Website': websites,
    	'Contract':,
    	'Community': community,
    	'Tags': tags,
    	}

    	for link in response.css('ul.coin-menu li.nav-item'):
    		if link.css('a.font-weight-bold.nav-link::text').get() == 'Historical Data':
    			historical_data_page = link.css('a.font-weight-bold.nav-link::attr(href)').get()
    			yield response.follow(next_page, callback=self.get_historical_data)

    def get_historical_data(self, response):
    	pass

