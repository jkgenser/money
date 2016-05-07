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
from models import Article



class ArticlePipeline(object):
    # def __init__(self):


    def process_item(self, item, spider):

        if db.session.query(Articles).get(item['article_id']) == None:
            db.session.add(Articles(**item))
            db.session.commit()
            print("article information added to db")

        else:
            print("article already in db, don't add to db")
