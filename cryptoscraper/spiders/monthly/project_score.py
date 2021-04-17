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
        	yield response.follow(url, callback=self.get_project_score, meta={'coin-id':int(coin)})

        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page is not None:
        	yield response.follow(next_page, callback=self.parse)

    def get_project_score(self, response):
        data = ProjectScoreItem()
        data['data_coin_id'] = response.meta['coin-id']
        try:
            data['team_score'] = response.css('div.text-lg::text')[0].get()
            data['eco_score'] = response.css('div.text-lg::text')[1].get()
            data['project_score'] = response.css('div.text-lg::text')[2].get()
            data['outlook'] = response.css('div.text-lg::text')[3].get()
            data['insight'] = response.css('div.text-3xs.mt-1::text').get()
        except IndexError:
            data['team_score'] = None
            data['eco_score'] = None
            data['project_score'] = None
            data['outlook'] = None
            data['insight'] = None           
        yield data
