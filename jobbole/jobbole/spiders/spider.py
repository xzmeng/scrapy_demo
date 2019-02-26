# -*- coding: utf-8 -*-
import scrapy
from ..items import ArticleItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        articles = response.css('.archive-title::attr(href)').getall()
        for article in articles:
            yield response.follow(article, callback=self.parse_article)
        next_page = response.css(".next::attr(href)").get()
        if next_page:
            yield response.follow(next_page)

    def parse_article(self, response):
        article = ArticleItem()
        article['title'] = response.css('h1::text').get()
        article['tag'] = response.css('.entry-meta a::text').get()
        article['body'] = response.css('.entry').get()
        yield article
