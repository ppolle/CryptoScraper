from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text, Numeric)
from sqlalchemy.dialects.postgresql import ARRAY 
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)

def recreate_database(engine):
    Base.metadata.drop_all(engine)
    base.metadata.create_all(engine)

class Coin(Base):
    __tablename__ = "coin"

    id = Column(Integer, primary_key=True)
    name = Column('name', Text())
    slug = Column('slug', Text())
    website = Column('website', ARRAY(String))#list
    coingecko = Column('coingecko', Text())
    community = Column('community', ARRAY(String))#list
    tags = Column('tags', ARRAY(String))#list
    data_coin_id = Column(Integer, unique=True)
    contract = Column(String)
    historical_data = relationship('HistoricalData', backref='coin')
    github_metrics = relationship('DailyGithubMetrics', backref='coin')
    social_metrics = relationship('DailySocialMetrics', backref='coin')
    project_scores = relationship('ProjectScore', backref='coin')
    coin_stats = relationship('DailyCoinStats', backref='coin')


class DailyGithubMetrics(Base):
    __tablename__ = "daily_github_metrics"

    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey('coin.id'))
    repo_name = Column('repo_name', String(150))
    url = Column(String)
    stars = Column('stars', Float)
    watchers = Column('watchers', Float)
    forks = Column('forks', Float)
    contributors = Column('contributors', Float)
    merged_pr = Column('merged_pr', Integer)
    closed_total_issue = Column('closed_total_issue', String(50))
    commits = Column('commits', Float)
    date = Column('date', Date)

class DailySocialMetrics(Base):
    __tablename__ = "daily_social_metrics"

    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey('coin.id'))
    date = Column('date', Date)
    redit_subscribers = Column('redit_subscribers', Integer)
    active_redit_ac = Column('active_redit_ac', Integer)
    avg_posts_per_hr = Column('avg_posts_per_hr', Float)
    avg_comments_per_hr = Column('avg_comments_per_hr', Float)
    twitter_followers = Column('twitter_followers', Integer)
    telegram_users = Column('telegram_users', Integer)

class Trending(Base):
    __tablename__ = "trending"

    id = Column(Integer, primary_key=True)
    coin = Column(String)
    slug = Column('slug', String(30))
    volume = Column('volume', Numeric)
    price = Column('price', Numeric)
    date = Column('date', Date)
    percentage_change = Column('percentage_change', String(50))

class HistoricalData(Base):
    __tablename__ = "historical_data"

    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey('coin.id'))
    date = Column('date', Date)
    market_cap = Column('market_cap', Float)
    volume = Column('volume', Float)
    market_open = Column('market_open', Float)
    market_close = Column('market_close', Float)

class DailyOverallMetrics(Base):
    __tablename__ = "daily_overall_metrics"

    id = Column(Integer, primary_key=True)
    coins = Column('coins', Integer)
    exchanges = Column('exchanges', Float)
    market_cap = Column('market_cap', Float)
    daily_vol = Column('daily_vol', Float)
    dominance = Column('dominance', ARRAY(String))
    eth_gas = Column('eth_gas', String(150))
    date = Column('date', Date)

class ProjectScore(Base):
    __tablename__ = "project_score"

    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey('coin.id'))
    date = Column('date', Date)
    team_score =Column('team_score', String(50))
    eco_sys_score = Column('eco_sys_score', String(50))
    project_score = Column('project_score', String(50))
    outlook = Column('outlook', String(50))
    insight = Column('insight', String(1000))

class DailyCoinStats(Base):
    __tablename__ = "daily_coin_stats"

    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey('coin.id'))
    date = Column('date', Date)
    price = Column('price', Float)
    price_percentage_change = Column('price_percentage_change', Float)
    percentage_change = Column(ARRAY(String))
    likes = Column(Float)
    circulating_supply = Column('circulating_supply', String(100))
    max_supply = Column('max_supply', Float)
    fully_diluted_valuation = Column('fully_diluted_valuation', Float)
    coin_roi = Column('coin_roi', Float)
    market_cap = Column('market_cap', Float)
    market_cap_dominance = Column('market_dominance', Float)
    trading_volume = Column('trading_volume', Float)
    volume_market_cap = Column('volume_market_cap', Float)
    daily_low_high = Column('daily_low_high', ARRAY(Float))
    weekly_low_high = Column('weekly_low_high',ARRAY(Float))
    market_cap_rank = Column('market_cap_rank', Float)
    all_time_high = Column('all_time_high', Float)
    all_time_high_date = Column('all_time_high_date', Date)
    ath_percent_change = Column('ath_percent_change', Float)
    all_time_low = Column('all_time_low', Float)
    all_time_low_date = Column('all_time_low_date', Date)
    atl_percent_change = Column('atl_percent_change', Float)

#circulating_supply = Column('circulating_supply', Float)