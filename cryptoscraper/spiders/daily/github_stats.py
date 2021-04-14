import scrapy


class GithubStatsSpider(scrapy.Spider):
    name = 'github_stats'
    allowed_domains = ['www.coingecko.com/en']
    start_urls = ['http://www.coingecko.com/en/']

    def parse(self, response):
        coins = response.css('tr td.pl-1.pr-0 i::attr(data-coin-id)').getall()

        for coin in coins:
        	url = "https://www.coingecko.com/en/coins/{}/developer_tab".format(coin)
        	yield response.follow(url, callback=self.get_github_stats)

        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page is not None:
        	yield response.follow(next_page, callback=self.parse)

    def get_github_stats(self, response):
    	pass