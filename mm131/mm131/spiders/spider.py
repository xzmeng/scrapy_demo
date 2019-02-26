# -*- coding: utf-8 -*-
import scrapy
from ..items import GirlItem, PictureItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['http://www.mm131.com/xinggan',
                  'http://www.mm131.com/qingchun/',
                  'http://www.mm131.com/qingchun/',
                  'http://www.mm131.com/xiaohua/',
                  'http://www.mm131.com/chemo/',
                  'http://www.mm131.com/qipao/',
                  'http://www.mm131.com/mingxing/', ]

    def parse(self, response):
        links = response.css('.list-left dd:not(.page) a::attr(href)').getall()
        for link in links:
            # to download picture, change parse_girl to parse_picture
            yield response.follow(link, callback=self.parse_girl)
        next_page = response.css('.page').re_first(r'.*<a href="(.*?)" class="page-en">下一页</a>')
        if next_page:
            yield response.follow(next_page)

    def parse_girl(self, response):
        girl_item = GirlItem()
        girl_item['title'] = response.css('h5::text').get()
        girl_item['count'] = response.css('.content-page .page-ch').re_first(r'共(\d+)页')
        yield girl_item

    def parse_picture(self, response):
        picture_item = PictureItem()
        picture_item['picture_title'] = response.css('h5::text').get()
        picture_item['image_urls'] = [response.css('.content-pic img::attr(src)').get()]
        yield picture_item
        next_page = response.css('.content-page .page-ch').re_first(r'.*<a href="(.*?)" class="page-ch">下一页</a>')
        if next_page:
            yield response.follow(next_page, callback=self.parse_picture)
