# -*- coding: utf-8 -*-
import scrapy
from alpha.items import ArticleList
from scrapy.selector import Selector
from scrapy import Spider


class AlphaSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["seekingalpha.com"]

    custom_settings = {
        'ARTICLE_LIST_PIPELINE_ENABLED': True
    }
    # First, construct a list of URLs to article list pages
    base_url = 'http://seekingalpha.com/articles?page='
    start_urls = []

    for i in range(2,5):
        next_link = base_url + str(i)
        start_urls.append(next_link)

    def parse(self, response):
        item = ArticleList()
        article_links = response.xpath('//*[@id="content_wrapper"]/div/div[2]/div[2]/div[2]/ul/*/div/a/@href').extract()
        # author_links = response.xpath('//*[@id="content_wrapper"]/div/div[2]/div[2]/div[2]/ul/*/div/div/a/@href').extract()
        # time_pub = response.xpath('//*[@id="content_wrapper"]/div/div[2]/div[2]/div[2]/ul/*/div/div/text()').extract()


        item['article_links'] = article_links
        # item['author_links'] = author_links
        # item['time_pub'] = time_pub

        return item

