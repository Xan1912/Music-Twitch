# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class RollingstoneItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    item_url = scrapy.Field()
    artist_name = scrapy.Field()
    img = scrapy.Field()
    author = scrapy.Field()
    publication_datetime = scrapy.Field()
    wiki_link = scrapy.Field()
    spotify_link = scrapy.Field()
    spotify_about = scrapy.Field()

    
