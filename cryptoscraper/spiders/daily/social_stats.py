import scrapy


class Daily/socialStatsSpider(scrapy.Spider):
    name = 'social_stats'
    allowed_domains = ['www.coingecko.com/en']
    start_urls = ['http://www.coingecko.com/en/']

    def parse(self, response):
        coins = response.css('tr td.pl-1.pr-0 i::attr(data-coin-id)').getall()

        for coin in coins:
        	url = "https://www.coingecko.com/en/coins/{}/social_tab".format(coin)
        	yield response.follow(url, callback=self.get_social_stats)

        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page is not None:
        	yield response.follow(next_page, callback=self.parse)

    def get_social_stat(self, response):
    	pass
