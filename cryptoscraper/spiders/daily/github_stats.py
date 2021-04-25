import scrapy
from cryptoscraper.items import GithubStatsItem
from cryptoscraper.utils import get_num, sanitize_string

class GithubStatsSpider(scrapy.Spider):
    name = 'github_stats'
    start_urls = ['http://www.coingecko.com/en/']

    def parse(self, response):
        coins = response.css('tr td.pl-1.pr-0 i::attr(data-coin-id)').getall()

        for coin in coins:
        	url = "https://www.coingecko.com/en/coins/{}/developer_tab".format(coin)
        	yield response.follow(url, callback=self.get_github_stats, meta={'data_coin_id':int(coin)})

        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page is not None:
        	yield response.follow(next_page, callback=self.parse)

    def get_github_stats(self, response):
        data = GithubStatsItem()
        data['data_coin_id'] = response.meta['data_coin_id']
        for github in response.css('div.card-block'):
            data['repo_name'] = github.css('span.text-xl a::text').get()
            data['url'] = github.css('span.text-xl a::attr(href)').get()
            data['stars'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[0].get())
            data['watchers'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[1].get())
            data['forks'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[2].get())
            data['contributors'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[3].get())
            data['merged_pr'] = get_num(github.css('div.pt-2.pb-2.font-light::text')[4].get())
            data['issues'] = sanitize_string(github.css('div.pt-2.pb-2.font-light::text')[5].get())

            yield data