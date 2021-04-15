import scrapy


class ProjectScoreSpider(scrapy.Spider):
    name = 'project_score'
    start_urls = ['https://www.coingecko.com/en/']

    def parse(self, response):
        coins = response.css('tr td.pl-1.pr-0 i::attr(data-coin-id)').getall()[:5]

        for coin in coins:
        	url = "https://www.coingecko.com/en/coins/{}/ratings_tab".format(coin)
        	yield response.follow(url, callback=self.get_project_score)

        # next_page = response.css('li.page-item.next a::attr(href)').get()
        # if next_page is not None:
        # 	yield response.follow(next_page, callback=self.parse)

    def get_project_score(self, response):
        try:
            yield {
        	'Team Score':response.css('div.text-lg::text')[0].get(),
        	'Eco System Score': response.css('div.text-lg::text')[1].get(),
        	'Project Score': response.css('div.text-lg::text')[2].get(),
        	'Outlook': response.css('div.text-lg::text')[3].get(),
        	'Insight': response.css('div.text-3xs.mt-1::text').get(),
        	}
        except IndexError:
           yield {
            'Team Score':None,
            'Eco System Score': None,
            'Project Score': None,
            'Outlook': None,
            'Insight': None,
            }