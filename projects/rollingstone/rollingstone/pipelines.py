# -*- coding: utf-8 -*-
from scrapy.exceptions import NotConfigured
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from rollingstone.models import Rollingstone, db_connect, create_rollingstone_table

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class RollingstonePipeline(object):
	"""RollingstonePipeline for storing scraped items in the database"""
	def __init__(self):
		"""
		Initializes database connection and sessionmaker.
		Creates rollingstone table. 
		"""
		engine = db_connect()
		create_rollingstone_table(engine)
		self.Session = sessionmaker(bind=engine)
	
	def process_item(self, item, spider):
		"""save items in the database This method is called for every item pipeline component."""
		session = self.Session()
		rollingstone = Rollingstone(**item)
#
		try:
			session.add(rollingstone)
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()
		
		return item











"""
class RollingstonePipeline(object):
	#Database connection
	with open("",r) as f:
		lines = f.read()
		HOSTNAME = lines
	def __init__self(self):
		self.conn = pymssql.connect(host=HOSTNAME,  user=USER, password=PASSWORD, database=DATABASE)
		self.cursor = self.conn.cursor()

	#pipeline items into database	
    def process_item(self, item, spider):
    	try:
    		self.cursor.execute("INSERT INTO rollingstones(title, artiste_name) VALUES (%s, %s)",
    			(item['title'], item['artiste_name']))
    		self.conn.commit()
    	except pymssql.Error, e:
    		print ("Error")
        return item
"""