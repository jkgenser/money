import scrapy
from app import db
from models import Article
from alpha import items
from datetime import datetime
from scrapy.selector import Selector
from scrapy.http.request import Request

class ParseArticleLogic(scrapy.Spider):

    def get_pub_date(self, selector):
        raw_date = selector.xpath('//*[@id="a-hd"]/div[1]/time/@content').extract()
        date = datetime.strptime(raw_date[0][:10], '%Y-%m-%d').date()
        return date


    def get_title(self, selector):
        title = selector.xpath('//*[@id="a-hd"]/h1/text()').extract()
        return str(title[0])


    def get_author(self, selector):
        author = selector.xpath('//*[@id="author-hd"]/div[2]/div[1]/a/span/text()').extract()
        try:
            return str(author[0])
        except:
            return 'no author listed'


    def get_author_url(self, selector):
        author_url = selector.xpath('//*[@id="author-hd"]/div[2]/div[1]/a/@href').extract()
        try:
            return str(author_url[0])
        except:
            return 'author url not listed'

    def get_summary(self, selector):
        summary = selector.xpath('//*[@id="a-cont"]/div[1]/div[@itemprop="description"]//p/text()').extract()
        return summary # as a list


    def get_body(self, selector):
        body = selector.xpath('//*[@id="a-body"]//text()').extract()
        return str(body)


    def get_covered(self, selector):
        covered = selector.xpath('//*[@id="about_primary_stocks"]/a/@href').extract()
        if covered == []:
            covered = selector.xpath('//*[@id="about_stocks"]/*/@href').extract()
        return covered


    def get_tags(self, selector):
        tags = selector.xpath('//*[@id="about-c"]/div[*]//span/text()').extract()
        return tags


    def process_item(self, item):

        if db.session.query(Article).get(item['article_id']) == None:
            db.session.add(Article(**item))
            db.session.commit()
            print("article added to db")
            return self.article_check()

        else:
            article = db.session.query(Article).get(item['article_id'])
            if article.title is None:
                article.article_url = item['article_url']
                article.pub_date = item['pub_date']
                article.title = item['title']
                article.author = item['author']
                article.author_url = item['author_url']
                article.summary = item['summary']
                article.covered = item['covered']
                article.body = item['body']
                article.tags = item['tags']
                db.session.commmit()
                print("article information updated updated in db")
                return self.article_check()

            else:
                print ("article info already in db, don't update")
                return self.article_check()