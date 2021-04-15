import scrapy


class DailySocialStatsSpider(scrapy.Spider):
    name = 'social_stats'
    allowed_domains = ['www.coingecko.com']
    start_urls = ['http://www.coingecko.com/en/']

    def parse(self, response):
        coins = response.css('tr td.pl-1.pr-0 i::attr(data-coin-id)').getall()[:1]

        for coin in coins:
        	url = "https://www.coingecko.com/en/coins/{}/social_tab".format(coin)
        	yield response.follow(url, callback=self.get_social_stats)

        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page is not None:
        	yield response.follow(next_page, callback=self.parse)

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