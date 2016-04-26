# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from models import ArticleLinks, db_connect, create_deals_table



class ArticleLinksPipeline(object):
    """Pipeline to store scraped items in the database"""

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Create articles table.
        """

        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """
        Save article links to the database.

        This method is called for every item pipeline component.
        """


        session = self.Session()
        article = ArticleLinks(**item)


        try:
            session.add(article)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


        return item
