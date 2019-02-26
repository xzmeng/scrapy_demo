# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class Mm131Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GirlItem(scrapy.Item):
    title = Field()
    count = Field()


class PictureItem(scrapy.Item):
    picture_title = Field()
    image_urls = Field()
    images = scrapy.Field()
