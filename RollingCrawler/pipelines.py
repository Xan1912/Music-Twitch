# import sys
# import MySQLdb
# import hashlib
# from scrapy.exceptions import NotConfigured
# from scrapy.exceptions import DropItem
# from scrapy.http import Request
# from scrapy.exceptions import DropItem


class RollingcrawlerPipeline(object):
    # def __init__(self):
    #     # the DB connection happens here
    #     self.conn = MySQLdb.connect('host', 'user', 'passwd', 
    #                                 'mydb', charset="utf8",
    #                                 use_unicode=True)
    #     self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        # Insert code here to check for duplicate URLS

        # Item scraped by the crawler is inserted to the database    
        # try:
        #     self.cursor.execute("""INSERT INTO rolling_stones (title, link, category, img)  
        #                 VALUES (%s, %s, %s, %s)""", 
        #                (item['title'].encode('utf-8'), 
        #                 item['link'].encode('utf-8'),
        #                 item['category'].encode('utf-8'),
        #                 item['img'].encode('utf-8')
        #                 )            
        #     self.conn.commit()
        # # Error handling            
        # except MySQLdb.Error, e:
        #     print("Error %d: %s" % (e.args[0], e.args[1]))

        return item
