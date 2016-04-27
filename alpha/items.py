# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleList(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_links = scrapy.Field()

    pass


class Article(scrapy.Item):
    '''
    Define attributes of the article item.
    '''
    article_id = scrapy.Field()
    pub_date = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    author_url = scrapy.Field()
    covered = scrapy.Field()
    article_url = scrapy.Field()