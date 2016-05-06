import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy import Spider
from app import db
from models import Article_urls

class ArticleSitemap(scrapy.Spider):

    name = 'article_sitemap'
    allowed_domains = ["seekingalpha.com"]
    start_urls = ['http://seekingalpha.com/sitemap_articles.xml']


    def parse(self, response):

        response.selector.remove_namespaces()
        article_urls = response.xpath('//urlset//url//loc//text()').extract()


        for url in article_urls:
            id = self.get_id(url)

            if db.session.query(Article_urls).get(id) == None:
                item = {}
                item['article_id'] = id
                item['url'] = url
                db.session.add(Article_urls(**item))
                db.session.commit()
                print('article: ' + id + ' has been loaded to db.')




    def get_id(self, url):
        id = url.split('/')[4].split('-')[0]
        return id



