from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
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


class Coin(Base):
    __tablename__ = "coin"

    id = Column(Integer, primary_key=True)
    name = Column('name', Text())
    slug = Column('slug', Text())
    website = Column('website', Text())
    coingecko = Column('coingecko', Text())
    community = Column('community', Text())#list
    tags = Column('tags', String(150))#list
    data_coin_id = Column(Integer, unique=True)


class DailyGithubMetrics(Base):
    __tablename__ = "daily_github_metrics"

    id = Column(Integer, primary_key=True)
    coin = Column(Integer, ForeignKey('coin.id'))
    repo_name = Column('repo_name', String(150))
    date = Column('date', Date)
    stars = Column('stars', Integer)
    watchers = Column('watchers', Integer)
    forks = Column('forks', Integer)
    contributors = Column('contributors', Integer)
    merged_pr = Column('merged_pr', Integer)
    closed_total_issue = Column('closed_total_issue', Integer)


class Trending(Base):
    __tablename__ = "trending"

    id = Column(Integer, primary_key=True)
    coin = Column(Integer, ForeignKey('coin.id'))
    slug = Column('slug', String(30), unique=True)
    volume = Column('volume', Integer)
    price = Column('price', Integer)
    percentage_change = Column('percentage_change', Integer)
    gain_loss = Column('gain_loss', Integer)


class HistoricalData(Base):
    __tablename__ = "historical_data"

    id = Column(Integer, primary_key=True)
    coin = Column(Integer, ForeignKey('coin.id'))
    date = Column('date', Date)
    market_cap = Column('market_cap', Integer)
    volume = Column('volume', Integer)
    market_open = Column('market_open', Integer)
    market_close = Column('market_close', Integer)

class DailyOverallMetrics(Base):
    __tablename__ = "daily_overall_metrics"

    id = Column(Integer, primary_key=True)
    coins = Column('coins', Integer)
    exchanges = Column('exchanges', Integer)
    market_cap = Column('market_cap', Integer)
    daily_vol = Column('daily_vol', Integer)
    dominance = Column('dominance', Text())
    eth_gas = Column('eth_gas', String(150))

class ProjectScore(Base):
    __tablename__ = "project_score"

    id = Column(Integer, primary_key=True)
    coin = Column(Integer, ForeignKey('coin.id'))
    date = Column('date', Date)
    team_score =Column('team_score', String(50))
    eco_sys_score = Column('eco_sys_score', String(50))
    project_score = Column('project_score', String(50))
    outlook = Column('outlook', String(50))
    insight = Column('insight', String(50))