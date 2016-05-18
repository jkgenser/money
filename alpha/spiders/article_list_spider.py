import scrapy
from app import db
from models import Article
from datetime import datetime
from scrapy.selector import Selector
from scrapy.http.request import Request

class ArticleSpider(scrapy.Spider):
    '''
    This class crawls through /articles and extracts every single article url
    that has ever been published on seekingalpha.

    Afer the article urls are extracted, they are later retrieved and parsed.
    '''
    name = "article_list"
    allowed_domains = "http://www.seekingalpha.com"
    start_urls = []

    # get all article IDs from the db
    query = db.session.query(Article.article_id).all()
    articles_in_db = set([article[0] for article in query])

    # construct of list of URLs to crawl
    for i in range(2,8000):
        start_urls.append('http://seekingalpha.com/articles?page=' + str(i))

    def parse(self, response):

        # grab list of article URLs on the page
        urls = response.xpath('//*[@id="content_wrapper"]/div/div[2]/div[2]/div[2]/ul/*/div/a/@href').extract()

        for url in urls:
            # make URL requestable
            full_url = self.allowed_domains + url
            article_id = int(url.split('/')[2].split('-')[0])

            # check if URL is in the database
            if db.session.query(Article).get(article_id) is not None:
                print('Article {} is already in the database, pass.'.format(str(article_id)))
                pass

            # add it to the database if the article_id is not in already
            else:
                article = {}
                article['article_id'] = int(article_id)
                article['article_url'] = full_url
                db.session.add(Article(**article))
                db.session.commit()
                print('Article {} has been added to the database.'.format(str(article_id)))
