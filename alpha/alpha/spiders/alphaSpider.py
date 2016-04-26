# -*- coding: utf-8 -*-
import scrapy
from alpha.items import Article
from scrapy.selector import Selector
from scrapy import Spider


class AlphaspiderSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["seekingalpha.com"]
    # start_urls = [
    #     'http://seekingalpha.com/articles',
    # ]


    # First, construct a list of URLs to article list pages
    base_url = 'http://seekingalpha.com/articles?page='
    start_urls = list()

    for i in range(2,10):
        next_link = base_url + str(i)
        start_urls.append(next_link)

    def parse(self, response):
        item = Article()
        article_links = response.xpath('//*[@id="content_wrapper"]/div/div[2]/div[2]/div[2]/ul/*/div/a/@href').extract()
        author_links = response.xpath('//*[@id="content_wrapper"]/div/div[2]/div[2]/div[2]/ul/*/div/div/a/@href').extract()
        time = response.xpath('//*[@id="content_wrapper"]/div/div[2]/div[2]/div[2]/ul/*/div/div/text()').extract()


        item['article_links'] = article_links
        item['author_links'] = author_links
        item['time_pub'] = time_pub

        return item

