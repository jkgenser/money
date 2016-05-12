import scrapy
from app import db
from models import Article
from datetime import datetime
from scrapy.selector import Selector
from scrapy.http.request import Request

# class ArticleSpider(ParseArticleLogic):
#     name = "$name"
#     allowed_domains = "http://wwww.seekingalpha.com"
#     start_urls = []
#
#     def parse(self, response):
#         pass

