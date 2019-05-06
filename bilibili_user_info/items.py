# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliUserInfoItem(scrapy.Item):
    # define the fields for your item here like:
    user_mid = scrapy.Field()
    user_uname = scrapy.Field()
    movies = scrapy.Field()
    user_url = scrapy.Field()
    pass
