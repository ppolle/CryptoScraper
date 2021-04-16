# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CryptoscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

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
	inisght = scrapy.Field()