from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.types import Date
from sqlalchemy.dialects.postgresql import ARRAY
# declarative_base() is a function that maps a class we define to a table structue in Postgres
# as well as a function that will take our metadata of our table to create the tables we need
Base = declarative_base()
metadata = MetaData()

def db_connect():
    """
    Performs database connection using database settings from settings.py
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**DATABASE))


def create_tables(engine):
    Base.metadata.create_all(engine)


class ArticleLinks(Base):
    """SQLAlchemy ArticleLinks model"""
    __tablename__ = "article_links"

    id = Column(Integer, primary_key=True)
    article_link = Column('article_link', String)


class ArticleMetaData(Base):
    __tablename__ = 'article_metadata'

    article_id = Column('article_id', Integer, primary_key=True)
    pub_date = Column('pub_date', Date)
    title = Column('title', String)
    author = Column('author', String)
    author_link = Column('author_link', String)
    covered = Column('covered', ARRAY(String))

# article_links = Table('article_links', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('article_link', String)
# )
#
#
#
# article_metadata = Table('article_metadata', metadata,
#     Column('article_id', Integer, primary_key=True),
#     Column('article_title', String),
#     Column('disclosure', String)
# )

