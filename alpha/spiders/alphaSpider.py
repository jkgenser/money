# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy import Spider
from alpha.items import Article
from datetime import datetime
import os
from app import db
from models import Articles

SEEKING_ALPHA_USERNAME = os.environ['SEEKING_ALPHA_USERNAME']
SEEKING_ALPHA_PASSWORD = os.environ['SEEKING_ALPHA_PASSWORD']

class AlphaSpider(scrapy.Spider):
    """
    This class defines the rules used to extract information from the urls we scrape.
    First, collect all of the urls of a page and then issue a request for each url.
    This request results in a page corresponding to a article from that list. Extract
    the relevant information from that article.
    """
    name = "article_list"
    allowed_domains = ["seekingalpha.com"]

    custom_settings = {
        'ARTICLE_LIST_PIPELINE_ENABLED': True
    }

    base_url = 'www.seekingalpha.com/'
    protocol = 'http'
    start_urls = ['http://seekingalpha.com/account/login']
    scrape_urls = []
    p_index = 0
    a_index = 0
    login_url1 = 'http://seekingalpha.com/account/email_preferences'
    login_url2 = 'http://seekingalpha.com/account/login?user_email=jerrygenser@gmail.com&slugs='
    article_urls = []

    for i in range(2,8000):
        scrape_urls.append('http://seekingalpha.com/articles?page=' + str(i))



    def parse(self, response):
        """
        First log into the website so that I see the correct version of articles
        """
        return scrapy.FormRequest.from_response(
            response,
            formxpath='//*[@id="orthodox_login"]',
            formdata={'user[email]': SEEKING_ALPHA_USERNAME, 'user[password]': SEEKING_ALPHA_PASSWORD},
            callback=self.after_login
        )


    def after_login(self, response):
        """
        Confirm login worked correctly; if so, then start crawling the list of articles
        """
        if response.request.url in [self.login_url1, self.login_url2]:
            print('Login succesful!', 'starting to scrape...')
            if self.p_index < len(self.scrape_urls):
                return Request(self.scrape_urls[self.p_index], callback=self.make_list)

        else:
            print('Login failed!')
            return


    def make_list(self, response):
        """
        For every url on the article list pages, extract the urls of the articles
        on those pages
        """
        sel = Selector(response)
        url_list = sel.xpath('//*[@id="content_wrapper"]/div/div[2]/div[2]/div[2]/ul/*/div/a/@href').extract()

        # Create a list of requestable URLs from the url list
        for url in url_list:
            self.article_urls.append(self.protocol + '://' + self.base_url + url)

        return self.article_check()


    def article_check(self):

        if self.a_index >= len(self.article_urls):
            self.a_index = 0
            self.p_index += 1
            return Request(self.login_url1, callback=self.after_login)

        else:
            if self.a_index < len(self.article_urls):
                article_id = self.article_urls[self.a_index].split('/')[5].split('-')[0]
                if db.session.query(Articles).get(article_id) == None:

                    return Request(self.article_urls[self.a_index], callback=self.parse_articles)
                else:
                    self.a_index += 1
                    return self.article_check()



    def parse_articles(self, response):
        """
        Parse each of the article urls generated by AlphaSpider.parse_list
        """

        sel = Selector(response)
        item = Article()
        item['article_id'] = response.request.url.split('/')[5].split('-')[0]
        item['article_url'] = str(response.request.url)
        item['pub_date'] = self.get_pub_date(sel)
        item['title'] = self.get_title(sel)
        item['author'] = self.get_author(sel)
        item['author_url'] = self.get_author_url(sel)
        item['summary'] = self.get_summary(sel)
        item['covered'] = self.get_covered(sel)
        item['body'] = self.get_body(sel)
        item['tags'] = self.get_tags(sel)

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        print(item)
        self.a_index += 1

        return item


    def get_pub_date(self, selector):
        raw_date = selector.xpath('//*[@id="a-hd"]/div[1]/time/@content').extract()
        date = datetime.strptime(raw_date[0][:10], '%Y-%m-%d').date()
        return date


    def get_title(self, selector):
        title = selector.xpath('//*[@id="a-hd"]/h1/text()').extract()
        return str(title[0])


    def get_author(self, selector):
        author = selector.xpath('//*[@id="author-hd"]/div[2]/div[1]/a/span/text()').extract()
        return str(author[0])


    def get_author_url(self, selector):
        author_url = selector.xpath('//*[@id="author-hd"]/div[2]/div[1]/a/@href').extract()
        return str(author_url[0])

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






