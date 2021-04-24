import scrapy
from cryptoscraper.utils import get_num, sanitize_string, get_name, get_slug

class DailyCoinStatsSpider(scrapy.Spider):
    name = 'coin_stats'
    start_urls = ['http://www.coingecko.com/en/']

    def parse(self, response):
    	coins = response.css('tr td.py-0.coin-name div.center a.d-lg-none.font-bold::attr(href)')[:15]

    	yield from response.follow_all(coins, callback=self.get_coin_data)

    	# navigate to the next page
    	# next_page = response.css('li.page-item.next a::attr(href)').get()
    	# if next_page is not None:
    	# 	yield response.follow(next_page, callback=self.parse)

    def get_coin_data(self, response):
        data = {}
        #core coin data
        data['coingecko'] = response.url
        data['name'] = get_name(response.css('h1.text-3xl::text').get())
        data['slug'] = get_slug(response.css('h1.text-3xl::text').get())
        data['data_coin_id'] = int(response.css('div.text-3xl span.no-wrap::attr(data-coin-id)').get())

        links = response.css('div.coin-link-row.mb-md-0')
        for link in links:
            if link.css('span.coin-link-title.mr-2::text').get() == 'Website':
                data['website'] = link.css('a.coin-link-tag::attr(href)').getall()

            if link.css('span.coin-link-title.mr-2::text').get() == 'Tags':
                data['tags'] = link.css('a.coin-link-tag::text').getall() + link.css('span.coin-tag.mr-1::text').getall()

            if link.css('span.coin-link-title.mr-2::text').get() == 'Community':
                data['community'] = link.css('a.coin-link-tag::attr(href)').getall()
            else:
                data['community'] = []

            if link.css('span.coin-link-title.mr-2::text').get() == 'Contract':
                data['contract'] = link.css('div.coin-tag.align-middle i::attr(data-address)').get()

        #daily coin stats
        data['coin_price'] = get_num(response.css('div.text-3xl span.no-wrap::text').get())
        data['percentage_change'] = sanitize_string(response.css('div.text-muted.text-normal div::text').get())
        data['likes'] = get_num(response.css('div.my-1.mt-1.mx-0 span.ml-1::text').get())
        
        for item in response.css('div.col-6.col-md-12.col-lg-6.p-0.mb-2'):
            if 'Circulating Supply' in item.css('div.font-weight-bold::text').get():
                data['circulating_supply'] = item.css('div.mt-1::text').get().strip()

            if 'Fully Diluted Valuation' in item.css('div.font-weight-bold::text').get():
                data['fully_diluted_valuation'] = get_num(item.css('div.mt-1 span::text').get().strip())

            if 'Max Supply' in item.css('div.font-weight-bold::text').get():
                data['max_supply'] = get_num(item.css('div.mt-1::text').get().strip())

            if 'Market Cap' in item.css('div.font-weight-bold::text').get():
                data['market_cap'] = get_num(item.css('div.mt-1::text').get().strip())

        for x in response.css('table.table.b-b tr'):
            if x.css('th::text').get() == '{} ROI'.format(data['name']):
                data['roi'] = x.css('td span::text').get().strip()
            else:
                data['roi'] = 0
            if x.css('th::text').get() == 'Market Cap Dominance':
                data['market_cap_dominance'] = x.css('td::text').get().strip()
            if x.css('th::text').get() == 'Volume / Market Cap':
                data['volume_market_cap'] = x.css('td::text').get().strip()
            if x.css('th::text').get() == 'Trading Volume':
                data['trading_volume'] = x.css('td span::text').get().strip()
            if x.css('th::text').get() == '24h Low / 24h High':
                data['24h_low_high'] = x.css('td span::text').get().strip()
            if x.css('th::text').get() == '7d Low / 7d High':
                data['7d_low_high'] = x.css('td span::text').get().strip()
            if x.css('th::text').get() == 'Market Cap Rank':
                data['market_cap_rank'] = x.css('td::text').get().strip()
            if x.css('th::text').get() == 'All-Time High':
                data['all_time_high'] = x.css('td span::text').get().strip()
                data['all_time_high_date'] = get_name(x.css('td small::text').get().strip())
            if x.css('th::text').get() == 'All-Time Low':
                data['all_time_low'] = x.css('td span::text').get().strip()
                data['all_time_low_date'] = get_name(x.css('td small::text').get().strip())

        yield data
