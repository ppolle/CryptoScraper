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
	data_coin_id = scrapy.Field()

class ProjectScoreItem(scrapy.Item):
	team_score = scrapy.Field()
	eco_score = scrapy.Field()
	project_score = scrapy.Field()
	outlook = scrapy.Field()
	insight = scrapy.Field()
	data_coin_id = scrapy.Field()

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
	
class GithubStatsItem(scrapy.Item):
	repo_name = scrapy.Field()
	stars = scrapy.Field()
	watchers = scrapy.Field()
	url = scrapy.Field()
	forks = scrapy.Field()
	contributors = scrapy.Field()
	merged_pr = scrapy.Field()
	issues = scrapy.Field()
	commits = scrapy.Field()
	data_coin_id = scrapy.Field()

class DailCoinStats(scrapy.Item):
	#coin items
	name = scrapy.Field()
	slug = scrapy.Field()
	website = scrapy.Field()
	coingecko = scrapy.Field()
	community = scrapy.Field()
	contract = scrapy.Field()
	data_coin_id = scrapy.Field()
	tags = scrapy.Field()
	#daily coin stats
	coin_price = scrapy.Field()
	price_percentage_change = scrapy.Field()
	percentage_change = scrapy.Field()
	btc_percentage_change = scrapy.Field()
	eth_percentage_change= scrapy.Field()
	likes = scrapy.Field()
	circulating_supply = scrapy.Field()
	fully_diluted_valuation = scrapy.Field()
	max_supply = scrapy.Field()
	market_cap = scrapy.Field()
	market_cap_dominance = scrapy.Field()
	coin_roi = scrapy.Field()
	volume_market_cap = scrapy.Field()
	trading_volume = scrapy.Field()
	daily_low_high = scrapy.Field()
	weekly_low_high = scrapy.Field()
	market_cap_rank = scrapy.Field()
	all_time_high = scrapy.Field()
	all_time_high_date = scrapy.Field()
	ath_percent_change = scrapy.Field()
	all_time_low = scrapy.Field()
	all_time_low_date = scrapy.Field()
	atl_percent_change = scrapy.Field()
	#daily_social_stats
	redit_subscribers = scrapy.Field()
	active_redit_ac = scrapy.Field()
	avg_posts_per_hr = scrapy.Field()
	avg_comments_per_hr = scrapy.Field()
	twitter_followers = scrapy.Field()
	telegram_users = scrapy.Field()

class CorrectionItems(scrapy.Item):
	coin_id = scrapy.Field()
	contract = scrapy.Field()
	community = scrapy.Field()






