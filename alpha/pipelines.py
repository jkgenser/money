# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from sqlalchemy.orm import sessionmaker
# from models import ArticleLinks, ArticleMetaData, db_connect, create_tables
# from scrapy.exceptions import NotConfigured
# from datetime import datetime
from app import db
from models import Articles




class ArticlePipeline(object):
    # def __init__(self):



    def process_item(self, item, spider):
        db.session.add(Articles(**item))
        db.session.commit()







# class ArticleLinksPipeline(object):
#     """Pipeline to store scraped items in the database"""
#
#     def __init__(self):
#         """
#         Initializes database connection and sessionmaker.
#         Emit create table commands.
#         """
#
#         engine = db_connect()
#         create_tables(engine)
#         self.Session = sessionmaker(bind=engine)
#
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         if not crawler.settings.getbool('ARTICLE_LIST_PIPELINE_ENABLED'):
#             raise NotConfigured
#         return cls()
#
#     def process_item(self, item, spider):
#         """
#         Save article links to the database.
#
#         This method is called for every item pipeline component.
#         """
#
#
#         session = self.Session()
#         # articlelink = ArticleLink(**item)
#
#         article_objects = []
#         for link in item['article_links']:
#             article_objects.append(ArticleLinks(article_link=link))
#             # article_link = ArticleLinks(article_link = link)
#
#         try:
#             # session.add(article_link)
#             session.bulk_save_objects(article_objects)
#             session.commit()
#
#         except:
#             session.rollback()
#             raise
#
#         finally:
#             session.close()
#
#
#         pass
#
#
# class SaveArticleInfoPipeline(object):
#
#     def __init__(self):
#
#         engine = db_connect()
#         create_tables(engine)
#         self.Session = sessionmaker(bind=engine)
#
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         if not crawler.settings.getbool('ARTICLE_META_PIPELINE_ENABLED'):
#             raise NotConfigured
#         return cls()
#
#
#     def process_item(self, item, spider):
#
#         session = self.Session()
#
#         try:
#             session.add(ArticleMetaData(**item))
#             session.commit()
#
#         except:
#             session.rollback()
#             raise
#
#         finally:
#             session.close()
#
#         pass
#
