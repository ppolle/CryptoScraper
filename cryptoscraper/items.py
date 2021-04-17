# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DailyOverallMetricsItem(scrapy.Item):
    coins = scrapy.Field()
    exchanges = scrapy.Field()
    market_cap = scrapy.Field()
    twenty_four_vol = scrapy.Field()
    dominance = scrapy.Field()
    eth_gas = scrapy.Field()

class TrendingItem(scrapy.Item):
	coin = scrapy.Field()
	coin_slug = scrapy.Field()
	volume = scrapy.Field()
	price = scrapy.Field()
	change24h = scrapy.Field()

class ProjectScoreItem(scrapy.Item):
	team_score = scrapy.Field()
	eco_score = scrapy.Field()
	project_score = scrapy.Field()
	outlook = scrapy.Field()
	insight = scrapy.Field()

class InitalScrapeItem(scrapy.Item):
	name = scrapy.Field()
	slug = scrapy.Field()
	website = scrapy.Field()
	coingecko = scrapy.Field()
	community = scrapy.Field()
	contract = scrapy.Field()
	data_coin_id = scrapy.Field()
	tags = scrapy.Field()
	market_cap = scrapy.Field()
	volume = scrapy.Field()
	market_open = scrapy.Field()
	market_close = scrapy.Field()
	date = scrapy.Field()
	


