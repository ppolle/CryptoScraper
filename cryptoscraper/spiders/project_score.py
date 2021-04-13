import scrapy


class ProjectScoreSpider(scrapy.Spider):
    name = 'project_score'
    allowed_domains = ['https://www.coingecko.com/en']
    start_urls = ['https://www.coingecko.com/en/']

    def parse(self, response):
        coins = response.css('tr td.py-0.coin-name div.center a.d-lg-none.font-bold::attr(href)').getall()

        for coin in coins:
        	url = "{}{}".format(coin,'#ratings')
        	yield response.follow(url, callback=self.get_project_score)

        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page is not None:
        	yield response.follow(next_page, callback=self.parse)

    def get_project_score(self, response):
    	yield {
    	'Team Score':response.css('div.text-lg.text-success::text')[0].get(),
    	'Eco System Score': response.css('div.text-lg.text-warning::text')[0].get(),
    	'Project Score': response.css('div.text-lg.text-warning::text')[1].get(),
    	'Outlook': response.css('div.text-lg.text-success::text')[1].get(),
    	'Insight': response.css('div.text-3xs.mt-1::text').get(),
    	}