# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Article(Item):
    '''
    Define attributes of the article item.
    '''
    article_id = Field()
    pub_date = Field()
    title = Field()
    author = Field()
    author_url = Field()
    covered = Field()
    article_url = Field()
    summary = Field()
    body = Field()
    tags = Field()