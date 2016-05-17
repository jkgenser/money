import scrapy
import os
from app import db
from models import Article
from datetime import datetime
from scrapy.selector import Selector
from scrapy.http.request import Request


class ArticleSpider(scrapy.Spider):
    name = "article_list"
    allowed_domains = "http://wwww.seekingalpha.com"
    query = Article.query.filter(Article.title==None).limit(5000).all() # get articles without title from db
    article_urls = [item.article_url for item in query]
    start_urls = ['http://seekingalpha.com/account/login']
    p_index = 0
    login_urls = ['http://seekingalpha.com/account/email_preferences']

    def parse(self, response):

        print(response.xpath('//body/@class').extract())
        return scrapy.FormRequest.from_response(
            response,
            formxpath='//*[@id="orthodox_login"]',
            formdata={'user[email]': os.environ['SEEKING_ALPHA_USERNAME'], 'user[password]': os.environ['SEEKING_ALPHA_PASSWORD']},
            callback=self.after_login,
            dont_filter=True,
            headers = {'X-Crawlera-Cookies': 'disable'}
        )


    def after_login(self, response):
        '''
        Confirm login worked correctly; if so, then start "controller" logic
        '''
        print(response.request.url)

        if response.request.url in self.login_urls:
            print('Login succesful!', 'starting to scrape...')
            return self.controller()

        else:
            print('Login failed!')
            print(response.request.url)
            return


    def controller(self):
        '''
        Crawling logic post-login
        Return this function after storing each object in the database
        '''
        if self.p_index < len(self.article_urls):
            return Request(self.article_urls[self.p_index], callback=self.parse_article, dont_filter=True,
                           headers = {'X-Crawlera-Cookies': 'disable'})


    def parse_article(self, response):
        '''
        Parse contents of each article using this function
        '''
        body_class = response.xpath('//body/@class').extract()
        print(body_class)
        print(self.get_tags(response))
        print(self.get_author(response))

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        article_id = response.request.url.split('/')[-1].split('-')[0]
        article = db.session.query(Article).get(article_id)

        if body_class[0] == 'embargo-pro-checkout pro force-pro logged-in':
            self.p_index += 1
            article.title = 'Pro login required'
            db.session.commit()
            return self.controller()

        if body_class[0] == 'author-research logged-in':
            self.p_index +=1
            article.title = 'Author research'
            db.session.commit()
            return self.controller()

        if article.title == None:
            article.pub_date = self.get_pub_date(response)
            article.title = self.get_title(response)
            article.author = self.get_author(response)
            article.author_url = self.get_author_url(response)
            article.summary = self.get_summary(response)
            article.covered = self.get_covered(response)
            article.body = self.get_body(response)
            article.tags = self.get_tags(response)
            db.session.commit()
            self.p_index += 1 # iterate to next article in the list of articles to request
            print('Article {} information has been added to the database.'.format(article_id))

        else:
            self.p_index += 1
            print('Article {} information is already in the database.'.format(article_id))
        return self.controller()


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