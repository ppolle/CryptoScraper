import scrapy
from scrapy.loader import ItemLoader
from cryptoscraper.items import ProjectScoreItem

class ProjectScoreSpider(scrapy.Spider):
    name = 'project_score'
    start_urls = ['https://www.coingecko.com/en/']

    def parse(self, response):
        coins = response.css('tr td.pl-1.pr-0 i::attr(data-coin-id)').getall()

        for coin in coins:
        	url = "https://www.coingecko.com/en/coins/{}/ratings_tab".format(coin)
        	yield response.follow(url, callback=self.get_project_score)

        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page is not None:
        	yield response.follow(next_page, callback=self.parse)

    def get_project_score(self, response):
        loader = ItemLoader(item=ProjectScoreItem, response=response)

     #    yield {
    	# 'team_score':response.css('div.text-lg::text')[0].get(),
    	# 'eco_score': response.css('div.text-lg::text')[1].get(),
    	# 'project_score': response.css('div.text-lg::text')[2].get(),
    	# 'outlook': response.css('div.text-lg::text')[3].get(),
    	# 'insight': response.css('div.text-3xs.mt-1::text').get(),
    	# }

        loader.add_value('team_score', response.css('div.text-lg::text')[0].get())
        loader.add_value('eco_score', response.css('div.text-lg::text')[1].get())
        loader.add_value('project_score', response.css('div.text-lg::text')[2].get())
        loader.add_value('outlook', response.css('div.text-lg::text')[3].get())
        loader.add_value('insight', response.css('div.text-3xs.mt-1::text').get())

        yield loader.load_item()