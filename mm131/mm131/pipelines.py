# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import pymongo
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline

from .items import GirlItem


class Mm131Pipeline(object):
    def process_item(self, item, spider):
        return item


class GirlItemPipeline:

    collection_name = 'girls'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, GirlItem):
            self.db[self.collection_name].insert_one(dict(item))
        return item


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        request_list = []
        for url in item.get(self.images_urls_field, []):
            request = Request(url)
            request.meta['picture_title'] = item['picture_title']
            request_list.append(request)
        return request_list

    def file_path(self, request, response=None, info=None):
        girl_title = request.meta.get('picture_title')
        match_obj = re.match(r'(.*)\((\d+)\)', girl_title)
        if match_obj:
            folder_name = match_obj.group(1)
            serial_num = match_obj.group(2)
        else:
            folder_name = girl_title
            serial_num = '1'
        return '{}/{}.jpg'.format(folder_name, serial_num)
