import scrapy
from sqlalchemy.orm import sessionmaker
from cryptoscraper.items import  DailCoinStats
from cryptoscraper.models import Coin, db_connect
from cryptoscraper.utils import get_num, sanitize_string, get_name, get_slug, get_date2

class DailyCoinStatsSpider(scrapy.Spider):
    name = 'coin_stats'
    start_urls = ['https://www.coingecko.com/en/']

    def __init__(self, *args, **kwargs):
        super(DailyCoinStatsSpider, self).__init__(*args, **kwargs)
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def parse(self, response):
        session = self.Session()
        coins = session.query(Coin).order_by(Coin.id).all()
        for coin in coins:
            yield response.follow(coin.coingecko, callback=self.get_coin_data)

    def get_circulating_max_supply(self, item):
        if item is not None:
            supplies = item.split('/')
            circulating_supply = get_num(supplies[0])
            max_supply = get_num(supplies[1])
            return {'circulating_supply': circulating_supply,'max_supply': max_supply}
        return None

    def get_percentage_change(self, value):
        percentage_change = []
        if len(value) > 0:
            for item in value:
                currency = sanitize_string(item.xpath('.//text()').get())
                change = item.xpath('.//span[@class="live-percent-change"]/span/text()').get()
                percentage_change.append("{} : {}".format(currency,change))

        return percentage_change

    def get_coin_data(self, response):
        data = DailCoinStats()
        #core coin data
        data['coingecko'] = response.url
        try:
            data['name'] = get_name(response.css('h1.text-3xl::text').get())
            data['slug'] = get_slug(response.css('h1.text-3xl::text').get())
        except TypeError:
            try:
                data['name'] = get_name(response.css('h1.mr-md-3::text').get())
                data['slug'] = get_slug(response.css('h1.mr-md-3::text').get())
            except TypeError:
                data['name'] = get_name(response.css('span.mx-2.text-3xl::text').get())
                data['slug'] = get_slug(response.css('span.mx-2.text-3xl::text').get())

        data['data_coin_id'] = int(response.xpath('//input[@name="coin_id"]/@value').get())
        data['contract'] = response.xpath('//i/@data-address').extract_first(default=None)

        links = response.css('div.coin-link-row.mb-md-0')
        for link in links:
            if link.css('span.coin-link-title.mr-2::text').get() == 'Website':
                data['website'] = link.css('div.tw-flex.flex-wrap a::attr(href)').getall()
  
            if link.css('span.tw-text-gray-500.mr-2::text').get() == 'Website':
                data['website']=link.css('a.tw-bg-gray-100.tw-rounded-md.tw-mx-1::attr(href)').getall()

            if link.css('span.coin-link-title.mr-2::text').get() == 'Tags':
                data['tags'] = link.css('div.tw-flex.flex-wrap a::text').getall() + link.css('span.coin-tag.mr-1::text').getall()

            if link.css('span.tw-text-gray-500.mr-2::text').get() == 'Tags':
                data['tags']=link.css('div.tw-font-normal span::text').getall()+link.css('a.tw-bg-gray-100.tw-rounded-md.tw-mx-1::text').getall()

            if link.css('span.coin-link-title.mr-2::text').get() == 'Community':
                data['community'] = link.css('div.tw-flex.flex-wrap a::attr(href)').getall()

            if link.css('span.tw-text-gray-500.mr-2::text').get() == 'Community':
                data['community']=link.css('a.tw-bg-gray-100::attr(href)').getall()


        #daily coin stats
        data['coin_price'] = get_num(response.css('div.text-3xl span.no-wrap::text').get())
        if data['coin_price'] is None:
            data['coin_price']=get_num(response.xpath('//span[@class="tw-text-gray-900 dark:tw-text-white"]/span[@data-target="price.price"]/text()').get())
        
        data['price_percentage_change'] = get_num(response.xpath('//span[@class="live-percent-change ml-1"]/span/text()').extract_first(default=None))
        data['likes'] = get_num(response.css('div.my-1.mt-1.mx-0 span.ml-1::text').get())
        change = response.xpath('//div[@class="text-muted text-normal"]/div')
        data['percentage_change'] = self.get_percentage_change(change)

        if len(data['percentage_change'])==0:
            change=response.xpath('//div[@class="tw-grid-cols-3 tw-mb-1 tw-flex"]/div[@class="tw-col-span-3 lg:tw-col-span-2"]/div[@class="tw-text-gray-500 text-normal"]/div')
            data['percentage_change']=self.get_percentage_change(change)
        
        for item in response.css('div.col-6.col-md-12.col-lg-6.p-0.mb-2'):
            if 'Circulating Supply' in item.css('div.font-weight-bold::text').get():
                supply = self.get_circulating_max_supply(item.css('div.mt-1::text').get().strip())
                if supply is not None:
                    data['circulating_supply'] = supply['circulating_supply']
                    data['max_supply'] = supply['max_supply']

            if 'Fully Diluted Valuation' in item.css('div.font-weight-bold::text').get():
                data['fully_diluted_valuation'] = get_num(item.css('div.mt-1 span::text').get())

        supply=response.xpath("//span[@class='tw-text-gray-900 dark:tw-text-white tw-float-right font-weight-bold tw-mr-1']/text()").getall()
        if len(supply) is not 0:
            data['circulating_supply']=get_num(supply[0])
            data['max_supply']=get_num(supply[1])

        for x in response.css('table.table.b-b tr'):

            if x.css('th::text').get() == '{} ROI'.format(data['name']):
                data['coin_roi'] = get_num(x.css('td span::text').get())
            if x.css('th::text').get() == "Market Cap":
                data['market_cap'] = get_num(x.css('td span::text').get())
            if x.css('th::text').get() == 'Market Cap Dominance':
                data['market_cap_dominance'] = get_num(x.css('td::text').get())
            if x.css('th::text').get() == 'Volume / Market Cap':
                data['volume_market_cap'] = get_num(x.css('td::text').get())
            if x.css('th::text').get() == 'Trading Volume':
                data['trading_volume'] = get_num(x.css('td span::text').get())
            if x.css('th::text').get() == '24h Low / 24h High':
                data['daily_low_high'] = [get_num(x) for x in x.css('td span::text').getall()]
            if x.css('th::text').get() == '7d Low / 7d High':
                data['weekly_low_high'] = [get_num(x) for x in x.css('td span::text').getall()]
            if x.css('th::text').get() == 'Market Cap Rank':
                data['market_cap_rank'] = get_num(x.css('td::text').get())
            if x.css('th::text').get() == 'All-Time High':
                data['all_time_high'] = get_num(x.css('td span::text').get())
                data['all_time_high_date'] = get_date2(get_name(x.css('td small::text').get().strip()))
                data['ath_percent_change'] = get_num(x.xpath('./td/span[@data-target="percent-change.percent"]/text()').get())
            if x.css('th::text').get() == 'All-Time Low':
                data['all_time_low'] = get_num(x.css('td span::text').get())
                data['all_time_low_date'] = get_date2(get_name(x.css('td small::text').get().strip()))
                data['atl_percent_change'] = get_num(x.xpath('./td/span[@data-target="percent-change.percent"]/text()').get())

        data['circulating_supply'] = data.get('circulating_supply', None)
        data['fully_diluted_valuation'] = data.get('fully_diluted_valuation', None)
        data['max_supply'] = data.get('max_supply', None)
        data['market_cap'] = data.get('market_cap', None)
        data['coin_roi'] = data.get('coin_roi', None)
        data['market_cap_dominance'] = data.get('market_cap_dominance', None)
        data['volume_market_cap'] = data.get('volume_market_cap', None)
        data['trading_volume'] = data.get('trading_volume', None)
        data['daily_low_high'] = data.get('daily_low_high', None)
        data['weekly_low_high'] = data.get('weekly_low_high', None)
        data['market_cap_rank'] = data.get('market_cap_rank', None)
        data['all_time_high'] = data.get('all_time_high', None)
        data['all_time_high_date'] = data.get('all_time_high_date', None)
        data['ath_percent_change'] = data.get('ath_percent_change', None)
        data['all_time_low'] = data.get('all_time_low', None)
        data['all_time_low_date'] = data.get('all_time_low_date', None)
        data['atl_percent_change'] =data.get('atl_percent_change', None)
        data['coin_price'] = data.get('coin_price', None)
        data['community'] = data.get('community', None)
        data['website'] = data.get('website', None)
        data['tags'] = data.get('tags', None)

        url = "https://www.coingecko.com/en/coins/{}/social_tab".format(data['data_coin_id'])
        yield response.follow(url, callback=self.get_social_stats, meta={'data':data})

    def get_social_stats(self, response):
        data= response.meta['data']
        for social in response.css('div.center.p-3'):
            if social.css('div.uppercase span::text').get() == 'Reddit Subscribers':
                data['redit_subscribers'] = get_num(social.css('div.mt-4.mb-2.text-2xl::text').get())

            if social.css('div.uppercase span::text').get() == 'Average Accounts Active':
                data['active_redit_ac'] = get_num(social.css('div.mt-3.mb-2.text-xl::text').get())

            if social.css('div.uppercase span::text').get() == 'Average New Hot Posts Per Hour':
                data['avg_posts_per_hr'] = get_num(social.css('div.mt-3.mb-2.text-xl::text').get())

            if social.css('div.uppercase span::text').get() == 'Average New Comments Per Hour':
                data['avg_comments_per_hr'] = get_num(social.css('div.mt-3.mb-2.text-xl::text').get())

            if social.css('div.uppercase span::text').get() == 'Twitter Followers':
                data['twitter_followers'] = get_num(social.css('div.mt-4.mb-2.text-2xl::text').get())

            if social.css('div.uppercase span::text').get() == 'Telegram Users':
                data['telegram_users'] = get_num(social.css('div.mt-4.mb-2.text-2xl::text').get())

        data['redit_subscribers']=data.get('redit_subscribers', None)
        data['active_redit_ac']=data.get('active_redit_ac', None)
        data['avg_posts_per_hr']=data.get('avg_posts_per_hr', None)
        data['avg_comments_per_hr']=data.get('avg_comments_per_hr', None)
        data['twitter_followers']=data.get('twitter_followers', None)
        data['telegram_users']=data.get('telegram_users', None)

        yield data
