import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy import Spider
from app import db
from models import Article

class ArticleSitemap(scrapy.Spider):

    name = 'article_sitemap'
    allowed_domains = ["seekingalpha.com"]
    start_urls = ['http://seekingalpha.com/sitemap_articles.xml']


    def parse(self, response):

        response.selector.remove_namespaces()
        article_urls = response.xpath('//urlset//url//loc//text()').extract()


        for url in article_urls:
            id = self.get_id(url)

            if db.session.query(Article).get(id) == None:
                article = {}
                article['article_id'] = id
                article['article_url'] = url
                db.session.add(Article(**article))
                db.session.commit()
                print('article_id: ' + id + ' has been loaded to db.')
            else:
                print('aritcle_id: ' + id + 'already in db.')


    def get_id(self, url):
        id = url.split('/')[4].split('-')[0]
        return id



