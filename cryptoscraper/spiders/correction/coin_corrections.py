import scrapy
from sqlalchemy.orm import sessionmaker
from cryptoscraper.items import CorrectionItems
from cryptoscraper.models import Coin, db_connect, create_table

class CoinCorrectionsSpider(scrapy.Spider):
    name = 'coin_corrections'
    allowed_domains = ['https://www.coingecko.com/en/']

    def __init__(self, *args, **kwargs):
        super(CoinCorrectionsSpider, self).__init__(*args, **kwargs)
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def start_requests(self):
        session = self.Session()
        coins = session.query(Coin).order_by(Coin.id).all()
        for coin in coins:
            yield scrapy.Request(coin.coingecko,
				    			method='GET',
				    			callback=self.parse,
				    			meta={'coin_id':coin.id})
        session.close()
 
    def parse(self, response):
        data = CorrectionItems()
        data['coin_id'] = response.meta['coin_id']
        data['contract'] = response.xpath('//div[@class="coin-tag align-middle"]/i/@data-address').extract_first(default='None')

        links = response.css('div.coin-link-row.mb-md-0')
        for link in links:
        	if link.css('span.coin-link-title.mr-2::text').get() == 'Community':
        		data['community'] = link.css('a.coin-link-tag::attr(href)').getall()

        data['community'] = data.get('community', [])
        yield data
