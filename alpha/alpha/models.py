from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE
from sqlalchemy import create_engine, Column, Integer, String, DateTime

# declarative_base() is a function that maps a class we define to a table structue in Postgres
# as well as a function that will take our metadata of our table to create the tables we need
DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**DATABASE))


def create_deals_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class ArticleLinks(DeclarativeBase):
    """SQLAlchemy ArticleLinks model"""
    __tablename__ = "article_links"

    id = Column(Integer, primary_key=True)
    article_link = Column('article_link', String)
    author_link = Column('author_link', String)
    time_pub = Column('time_pub', DateTime, nullable=True)
