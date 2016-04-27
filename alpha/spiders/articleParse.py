# import scrapy
# from alpha.items import Article
# from scrapy.selector import Selector
# from scrapy import Spider
# from sqlalchemy.orm import sessionmaker
# from alpha.models import ArticleLinks, db_connect, create_tables
# from datetime import datetime
#
# class articleParse(scrapy.Spider):
#     name = 'article_parse'
#     allowed_domains = ['seekingalpha.com']
#
#     custom_settings = {
#         'ARTICLE_META_PIPELINE_ENABLED': True
#     }
#     start_urls = []
#     # connect to db
#
#
#     engine = db_connect()
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#
#
#     for obj in session.query(ArticleLinks):
#         link = 'http://seekingalpha.com' + obj.article_link
#         start_urls.append(link)
#
#         session.close()
#
#     start_urls = start_urls[:5]
#     print('start_urls_here:', start_urls)
#
#     def parse(self, response):
#         item = Article()
#         raw_date = response.xpath('//*[@id="a-hd"]/div[1]/time/@content').extract()
#         print("this is raw_date:", raw_date)
#         date_obj = datetime.strptime(raw_date[0][:10], "%Y-%m-%d").date()
#         print("this is date_obj:", date_obj)
#         item['pub_date'] = date_obj
#         item['title'] = response.xpath('//*[@id="a-hd"]/h1/text()').extract()
#         item['author'] = response.xpath('//*[@id="author-hd"]/div[2]/div[1]/a/span/text()').extract()
#         item['author_link'] = response.xpath('//*[@id="author-hd"]/div[2]/div[1]/a/@href').extract()
#         item['covered'] = response.xpath('//*[@id="about_primary_stocks"]/a/@href').extract()
#         # If there are multiple stocks, subsequent stocks usually nested under id=about_stocks
#         # rather than id=about_primary_stocks
#         if item['covered'] == []:
#             item['covered'] = response.xpath('//*[@id="about_stocks"]/*/@href').extract()
#
#         return item


    # get URLs from Postgres db
