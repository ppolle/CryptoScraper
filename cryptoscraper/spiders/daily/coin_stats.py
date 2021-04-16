import scrapy


class DailyCoinStatsSpider(scrapy.Spider):
    name = 'coin_stats'
    start_urls = ['http://www.coingecko.com/en/']

    def parse(self, response):
    	coins = response.css('tr td.py-0.coin-name div.center a.d-lg-none.font-bold::attr(href)')

    	yield from response.follow_all(coins, callback=self.get_coin_data)

    	# navigate to the next page
    	next_page = response.css('li.page-item.next a::attr(href)').get()
    	if next_page is not None:
    		yield response.follow(next_page, callback=self.parse)

    def get_coin_data(self, response):
    	data = {}

    	data['coin_price'] = response.css('div.text-3xl::text').get()
    	data['percentage_change'] = response.css('div.text-muted.text-normal div::text').get()
    	data['likes'] = response.css('div.my-1.mt-1.mx-0 span.ml-1::text').get()

    	for item in response.css('div.col-6.col-md-12.col-lg-6.p-0.mb-2'):

    		if item.css('div.font-weight-bold::text').get() == 'Circulating Supply':
    			data['circulating_supply'] = item.css('div.mt-1::text').get()

    		if item.css('div.font-weight-bold::text').get() == 'Fully Diluted Valuation':
    			data['fully_diluted_valuation'] = item.css('div.mt-1::text').get()

    		if item.css('div.font-weight-bold::text').get() == 'Max Supply':
    			data['max_supply'] = item.css('div.mt-1::text').get()

    	for detail in response.css('table.table.b-b'):
    		if 'ROI' in detail.css('th::text').get():
    			data['roi'] = detail.css('td::text').get()

    		if detail.css('th::text').get() == 'Market Cap':
    			data['market_cap'] = detail.css('td::text').get()

    		if detail.css('th::text').get() == 'Market Cap Dominance':
    			data['market_cap_dominance'] = detail.css('td::text').get()

    		if detail.css('th::text').get() == 'Volume / Market Cap':
    			data['volume_market_cap'] = detail.css('td::text').get()
    		
    		if detail.css('th::text').get() == 'Trading Volume':
    			data['trading_volume'] = detail.css('td::text').get()

    		if detail.css('th::text').get() == '24h Low / 24h High':
    			data['24h_low_high'] = detail.css('td::text').get()

    		if detail.css('th::text').get() == '7d Low / 7d High':
    			data['7d_low_high'] = detail.css('td::text').get()

    		if detail.css('th::text').get() == 'Market Cap Rank':
    			data['market_cap_rank'] = detail.css('td::text').get()

    		if detail.css('th::text').get() == 'All-Time High':
    			data['all_time_high'] = detail.css('td::text').get()

    		if detail.css('th::text').get() == 'All-Time Low':
    			data['market_cap_dominance'] = detail.css('td::text').get()

    	yield data

    def get_social_stats(self, response):
        data= {}
        for social in response.css('div.center.p-3'):
            if social.css('div.uppercase span::text').get() == 'Reddit Subscribers':
                data['redit_subscribers'] = social.css('div.mt-4.mb-2.text-2xl::text').get()

            if social.css('div.uppercase span::text').get() == 'Average Accounts Active':
                data['active_redit_ac'] = social.css('div.mt-3.mb-2.text-xl::text').get()

            if social.css('div.uppercase span::text').get() == 'Average New Hot Posts Per Hour':
                data['avg_posts_per_hr'] = social.css('div.mt-3.mb-2.text-xl::text').get()

            if social.css('div.uppercase span::text').get() == 'Average New Comments Per Hour':
                data['avg_comments_per_hr'] = social.css('div.mt-3.mb-2.text-xl::text').get()

            if social.css('div.uppercase span::text').get() == 'Twitter Followers':
                data['twitter_followers'] = social.css('div.mt-4.mb-2.text-2xl::text').get()

            if social.css('div.uppercase span::text').get() == 'Telegram Users':
                data['telegram_users'] = social.css('div.mt-4.mb-2.text-2xl::text').get()

        yield data

    def get_github_stats(self, response):
        data = {}
        for github in response.css('div.card-block'):
            data['repo_name'] = github.css('span.text-xl a::text').get()
            data['url'] = github.css('span.text-xl a::attr(href)').get()
            data['stars'] = github.css('div.pt-2.pb-2.font-light::text')[0].get()
            data['watchers'] = github.css('div.pt-2.pb-2.font-light::text')[1].get()
            data['forks'] = github.css('div.pt-2.pb-2.font-light::text')[2].get()
            data['contributors'] = github.css('div.pt-2.pb-2.font-light::text')[3].get()
            data['merger_pr'] = github.css('div.pt-2.pb-2.font-light::text')[4].get()
            data['issues'] = github.css('div.pt-2.pb-2.font-light::text')[5].get()

            yield data