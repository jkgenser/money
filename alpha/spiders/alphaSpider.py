# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy import Spider
from alpha import items
from alpha.spiders.parse_article_html import ParseArticleLogic
from datetime import datetime
import os
from app import db
from models import Article


class AlphaSpider(ParseArticleLogic):
    """
    This class defines the rules used to extract information from the urls we scrape.
    First, collect all of the urls of a page and then issue a request for each url.
    This request results in a page corresponding to a article from that list. Extract
    the relevant information from that article.
    """
    name = "article"
    allowed_domains = ["seekingalpha.com"]

    custom_settings = {
        'ARTICLE_LIST_PIPELINE_ENABLED': True
    }

    base_url = 'www.seekingalpha.com'
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
            formdata={'user[email]': os.environ['SEEKING_ALPHA_USERNAME'], 'user[password]': os.environ['SEEKING_ALPHA_PASSWORD']},
            callback=self.after_login,
            dont_filter=True
        )


    def after_login(self, response):
        """
        Confirm login worked correctly; if so, then start crawling the list of articles
        """
        if response.request.url in [self.login_url1, self.login_url2]:
            print('Login succesful!', 'starting to scrape...')
            if self.p_index < len(self.scrape_urls):
                return Request(self.scrape_urls[self.p_index], callback=self.make_list, dont_filter=True)

        else:
            print('Login failed!')
            print(response.request.url)
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

        if self.a_index >= len(self.article_urls):  # if all of the articles in the list have been parsed
            self.a_index = 0                        # reset the article list index
            self.article_urls = []                  # delete elements in the current article list
            self.p_index += 1                       # increment article page index
            return Request(self.login_url2, callback=self.after_login)

        else:
            if self.a_index < len(self.article_urls):
                article_id = self.article_urls[self.a_index].split('/')[5].split('-')[0]
                article = db.session.query(Article).get(article_id)

                if article == None:
                    print ("Article " + article_id + " is not in the database, making a request.")
                    return Request(self.article_urls[self.a_index], callback=self.parse_article)

                else:
                    if article.title == None:
                        print ("Article " + article_id + " is in database but no information, making a request")
                        return Request(self.article_urls[self.a_index], callback=self.parse_article)

                    else:
                        print("Article information for " + article_id + " in the database, don't make a request")
                        self.a_index += 1
                        return self.article_check()













