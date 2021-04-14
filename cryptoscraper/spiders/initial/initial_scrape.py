import scrapy


class InitialScrapeSpider(scrapy.Spider):
    name = 'initial_scrape'
    start_urls = ['https://www.coingecko.com/en/']

    def historical_date_format(self, url):
    	from datetime import datetime

    	todays_date = datetime.today().strftime('%Y-%m-%d')
    	additional_url = "?end_date={}&start_date=2007-01-01#panel".format(todays_date)

    	return "{}{}".format(url.replace('#panel',''), additional_url)

    def parse(self, response):
    	#navigate to respective coins to extract individual coin data
    	coins = response.css('tr td.py-0.coin-name div.center a.d-lg-none.font-bold::attr(href)')

    	yield from response.follow_all(coins, callback=self.get_coin_data)

    	#navigate to the next page
    	next_page = response.css('li.page-item.next a::attr(href)').get()
    	if next_page is not None:
    		yield response.follow(next_page, callback=self.parse)

    def get_coin_data(self, response):
    	data = {}
    	data['Name'] = response.css('h1.mr-md-3.mx-2.mb-md-0.text-3xl.font-semibold::text').get()
    	links = response.css('div.coin-link-row.mb-md-0')
    	for link in links:
    		if link.css('span.coin-link-title.mr-2::text').get() == 'Website':
    			data['Website'] = link.css('a.coin-link-tag::attr(href)').getall()

    		if link.css('span.coin-link-title.mr-2::text').get() == 'Tags':
    			data['Tags'] = link.css('a.coin-link-tag::attr(href)').getall() + link.css('span.coin-tag.mr-1::text').getall()

    		if link.css('span.coin-link-title.mr-2::text').get() == 'Community':
    			data['Community'] = link.css('a.coin-link-tag::attr(href)').getall()

    		if link.css('span.coin-link-title.mr-2::text').get() == 'Community':
    			data['Contract'] = link.css('div.coin-tag.align-middle i::attr(data-address)').get()

    	yield data

    	for link in response.css('ul.coin-menu li.nav-item'):
    		if link.css('a.font-weight-bold.nav-link::text').get() == 'Historical Data':
    			historical_data_page = link.css('a.font-weight-bold.nav-link::attr(href)').get()
    			url = self.historical_date_format(historical_data_page)
    			yield response.follow(url, self.get_historical_data)

    def get_historical_data(self, response):

    	for data in response.css('tbody tr'):
    		yield {
    			  'Date': data.css('th::text').get(),
    			  'Market Cap': data.css('td::text')[0].get(),
    			  'Volume': data.css('td::text')[1].get(),
    			  'Open': data.css('td::text')[2].get(),
    			  'Close': data.css('td::text')[3].get()
    			  }

