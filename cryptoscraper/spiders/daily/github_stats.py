import scrapy


class GithubStatsSpider(scrapy.Spider):
    name = 'github_stats'
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