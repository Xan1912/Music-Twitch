import scrapy

class RollingcrawlerItem(scrapy.Item):
    
    # Defining the fields to scrape:

    titles = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    img = scrapy.Field()
