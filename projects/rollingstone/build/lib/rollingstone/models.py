from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime
import rollingstone.settings
#

DeclarativeBase = declarative_base()

	
def db_connect():
	"""
		Performs database sonnection using dataabase settings from the settings.py
		Returns sqlalchemy engine 
	"""
	return create_engine(URL(**rollingstone.settings.DATABASE))

#create table
def create_rollingstone_table(engine):
	""""""
	DeclarativeBase.metadata.create_all(engine)


#create database fields
class Rollingstone(DeclarativeBase):
	""" Sqlalchemy rollingstones model"""
	__tablename__ = "rollingstone" #table name in database
	#columns of the table as defined in the items file.
	id = Column(Integer, primary_key=True)
	title = Column('title', String)
	item_url = Column('item_url', String, nullable=True)
	artist_name = Column('artist_name', String, nullable=True)
	img = Column('img', String, nullable=True)
	author = Column('author', String, nullable=True)
	publication_datetime = Column('publication_datetime', DateTime, nullable=True)
	wiki_link = Column('wiki_link', String, nullable=True)
	spotify_link = Column('spotify_link', String, nullable=True)
	spotify_about = Column('spotify_about', String, nullable=True)