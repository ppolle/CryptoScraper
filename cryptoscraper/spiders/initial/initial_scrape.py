import scrapy
from cryptoscraper.items import InitalScrapeItem
from cryptoscraper.utils import get_slug, get_name, get_num, get_date

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
    	coins = response.css('tr td.py-0.coin-name div.center a.d-lg-none.font-bold::attr(href)')[:15]

    	yield from response.follow_all(coins, callback=self.get_coin_data)

    	#navigate to the next page
    	next_page = response.css('li.page-item.next a::attr(href)').get()
    	if next_page is not None:
    		yield response.follow(next_page, callback=self.parse)

    def get_coin_data(self, response):
        data = InitalScrapeItem()
        data['coingecko'] = response.url
        data['name'] = get_name(response.css('h1.mr-md-3.mx-2.mb-md-0.text-3xl.font-semibold::text').get())
        data['slug'] = get_slug(response.css('h1.mr-md-3.mx-2.mb-md-0.text-3xl.font-semibold::text').get())
        data['data_coin_id'] = int(response.css('div.text-3xl span.no-wrap::attr(data-coin-id)').get())

        links = response.css('div.coin-link-row.mb-md-0')
        for link in links:
            if link.css('span.coin-link-title.mr-2::text').get() == 'Website':
                data['website'] = link.css('a.coin-link-tag::attr(href)').getall()

            if link.css('span.coin-link-title.mr-2::text').get() == 'Tags':
                data['tags'] = link.css('a.coin-link-tag::text').getall() + link.css('span.coin-tag.mr-1::text').getall()

            if link.css('span.coin-link-title.mr-2::text').get() == 'Community':
                data['community'] = link.css('a.coin-link-tag::attr(href)').getall()

            if link.css('span.coin-link-title.mr-2::text').get() == 'Contract':
                data['contract'] = link.css('div.coin-tag.align-middle i::attr(data-address)').get()

        for link in response.css('ul.coin-menu li.nav-item'):
            if link.css('a.font-weight-bold.nav-link::text').get() == 'Historical Data':
                historical_data_page = link.css('a.font-weight-bold.nav-link::attr(href)').get()
                url = self.historical_date_format(historical_data_page)
                yield response.follow(url, self.get_historical_data, meta={'coin_item':data})

    def get_historical_data(self, response):
        item = response.meta['coin_item']
        for data in response.css('tbody tr'):
            item['date'] = get_date(data.css('th::text').get())
            item['market_cap'] = get_num(data.css('td::text')[0].get())
            item['volume'] = get_num(data.css('td::text')[1].get())
            item['market_open'] = get_num(data.css('td::text')[2].get())
            item['market_close'] = get_num(data.css('td::text')[3].get())

            yield item
    			  

