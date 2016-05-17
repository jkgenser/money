# import scrapy
# from app import db
# from models import Article
# from alpha import items
# from datetime import datetime
# from scrapy.selector import Selector
# from scrapy.http.request import Request
#
# class ParseArticleLogic(scrapy.Spider):
#
#
#     def get_pub_date(self, selector):
#         raw_date = selector.xpath('//*[@id="a-hd"]/div[1]/time/@content').extract()
#         date = datetime.strptime(raw_date[0][:10], '%Y-%m-%d').date()
#         return date
#
#
#     def get_title(self, selector):
#         title = selector.xpath('//*[@id="a-hd"]/h1/text()').extract()
#         return str(title[0])
#
#
#     def get_author(self, selector):
#         author = selector.xpath('//*[@id="author-hd"]/div[2]/div[1]/a/span/text()').extract()
#         try:
#             return str(author[0])
#         except:
#             return 'no author listed'
#
#
#     def get_author_url(self, selector):
#         author_url = selector.xpath('//*[@id="author-hd"]/div[2]/div[1]/a/@href').extract()
#         try:
#             return str(author_url[0])
#         except:
#             return 'author url not listed'
#
#     def get_summary(self, selector):
#         summary = selector.xpath('//*[@id="a-cont"]/div[1]/div[@itemprop="description"]//p/text()').extract()
#         return summary # as a list
#
#
#     def get_body(self, selector):
#         body = selector.xpath('//*[@id="a-body"]//text()').extract()
#         return str(body)
#
#
#     def get_covered(self, selector):
#         covered = selector.xpath('//*[@id="about_primary_stocks"]/a/@href').extract()
#         if covered == []:
#             covered = selector.xpath('//*[@id="about_stocks"]/*/@href').extract()
#         return covered
#
#
#     def get_tags(self, selector):
#         tags = selector.xpath('//*[@id="about-c"]/div[*]//span/text()').extract()
#         return tags
#

    # def process_item(self, item):
    #
    #     if db.session.query(Article).get(item['article_id']) ==
    #
    #     # if db.session.query(Article).get(item['article_id']) == None:
    #     #     db.session.add(Article(**item))
    #     #     db.session.commit()
    #     #     print("article " + str(item['article_id']) + " added to db")
    #     #     return self.article_check()
    #     #
    #     # else:
    #     #     article = db.session.query(Article).get(item['article_id'])
    #     #     if article.title is None:
    #     #         article.article_url = item['article_url']
    #     #         article.pub_date = item['pub_date']
    #     #         article.title = item['title']
    #     #         article.author = item['author']
    #     #         article.author_url = item['author_url']
    #     #         article.summary = item['summary']
    #     #         article.covered = item['covered']
    #     #         article.body = item['body']
    #     #         article.tags = item['tags']
    #     #         db.session.commmit()
    #     #         print("article " + str(article.article_id) + " updated in db")
    #     #         return self.article_check()
    #     #
    #     #     else:
    #     #         print ("article info for " + str(article.article_id) + " already in db, don't update")
    #     #         return self.article_check()
    #
    #
    # def parse_article(self, response):
    #     """
    #     Parse each of the article urls generated by AlphaSpider.parse_list
    #     """
    #
    #     sel = Selector(response)
    #     item = {}
    #     item['article_id'] = response.request.url.split('/')[5].split('-')[0]
    #     item['article_url'] = str(response.request.url)
    #     item['pub_date'] = self.get_pub_date(sel)
    #     item['title'] = self.get_title(sel)
    #     item['author'] = self.get_author(sel)
    #     item['author_url'] = self.get_author_url(sel)
    #     item['summary'] = self.get_summary(sel)
    #     item['covered'] = self.get_covered(sel)
    #     item['body'] = self.get_body(sel)
    #     item['tags'] = self.get_tags(sel)
    #
    #     # from scrapy.shell import inspect_response
    #     # inspect_response(response, self)
    #     print('Article ' + item['article_id'] + ' has been parsed.')
    #     self.a_index += 1
    #     return self.process_item(item)