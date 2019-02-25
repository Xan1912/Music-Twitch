# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import re

from rollingstone.items import RollingstoneItem

import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials



class RedditbotSpider(scrapy.Spider):
    name = 'rollingstone'
    allowed_domains = ['www.rollingstone.com']
    start_urls = ['https://www.rollingstone.com/music/']


    #def __init__(self, category=None, *args, **kwargs):
     #   super(RedditbotSpider, self).__init__(*args, **kwargs)


    def parse(self, response):

        urls = response.xpath('//div[@class="l-blog__item l-blog__item--spacer-s"]/ul/li/article/a/@href').extract()
        
        
        for url in urls:
            
            request = scrapy.Request(url, callback=self.parse_inner)
            
            yield request
            
        # ----------------------------------- Redirections to the next page --------------------------------------------
        
        next_page = response.xpath('//*[@id="site_wrap"]/div[3]/div[1]/main/div[4]/div/a[2]/@href').extract()
        
        # ----------------------------------- Double check if next_page is not empty ------------------------------------
        
        if next_page == []: 
            next_page = response.xpath('//*[@id="site_wrap"]/div[3]/div[1]/main/div[4]/div/a[1]/@href').extract()
        
        # ----------------------------------- Assign the URL to the next page to start the crawl again ------------------

        if next_page:
            next_href = next_page[0]
            next_page_url = next_href
            request = scrapy.Request(url=next_page_url)
            yield request
    
    def parse_inner(self,response):

        # ----------------------------------- Authorization for Spotify ----------------------------------------------------

        client_credentials_manager = SpotifyClientCredentials(client_id='b7cf2f5f0e074d1ca984a546822797cc',
                        client_secret='c435b02f49304b7db74ec08ddb7df6e7')

        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # ----------------------------------- Setting the fields and passing the scraped data -----------------------------------

        
        
        # ----------------------------------- Title ----------------------------------------------------
        
        title = response.xpath('//*[@id="site_wrap"]/div[2]/div/main/article/header/h1/text()').extract()[0].replace('\n', '').replace('\t', '')
        
        # ----------------------------------- author of the news ---------------------------------------
        
        author = response.xpath('//div[@class="c-byline__author"]/a/text()').extract()[0].replace('\n', '').replace('\t', '')

        # ----------------------------------- Artist Name ----------------------------------------------
        
        artist_name = response.xpath('//*[@id="site_wrap"]/div[2]/div/main/article/div/footer/div[1]/p/a/text()').extract()
        
        # ----------------------------------- Img ----------------------------------------------
        img = response.xpath('//*[@id="site_wrap"]/div[2]/div/main/article/figure/div[1]/div/img/@data-src').extract()
        if img:
            img = img[0]
        else:
            img = ''

        # ----------------------------------- Artist Name ----------------------------------------------
        
        artist_name = response.xpath('//*[@id="site_wrap"]/div[2]/div/main/article/div/footer/div[1]/p/a/text()').extract()
        
        if artist_name:
            artist_name = artist_name[0].replace('\n', '').replace('\t', '')
        else:
            artist_name = ''
        
        
        # ----------------------------------- Wiki link mark up ----------------------------------------
        
        if artist_name != '':

            inbuilt_wiki_uri = 'https://en.wikipedia.org/wiki/'

            wiki_link = inbuilt_wiki_uri + "_".join(artist_name.split(' '))
        
        else:
            wiki_link = ''        
        
        # ----------------------------------- publication datetime --------------------------------------
        
        publication_datetime = response.xpath('//*[@id="site_wrap"]/div[2]/div/main/article/header/time/text()').extract()[0].replace('\n', '').replace('\t', '').replace('ET','')
        

        spotify_link = ''
        spotify_about = ''

        
        # ------------------------------------------- Collecting spotify data -----------------------------------
        
        if artist_name:
            
            name = artist_name
            results = spotify.search(q='artist:' + name, type='artist')
            items = results['artists']['items']
            
            if len(items) > 0:
                # ----------------------------------- Link to the index page of the Artist in Spotify -----------------------------------
                spotify_link = items[0]['external_urls']['spotify']

                # ----------------------------------- Link to the about page of the Artist -----------------------------------
                spotify_about = spotify_link + '/about'
        
        # ------------------------------------ Descripiton --------------------------------------------
        if spotify_link == '':
            spotify_link = 'Artiste has no spotify link'

        if spotify_about == '':
            spotify_about = 'Artiste has no spotify about'
        # ----------------------------------- Making a dictionary of the scraped data --------------------

        # item['title'] = title
        # item['item_url'] = response.url
        # item['artist_name'] = artist_name

        # yield item
        

        if img == '':
            yield None
        
        elif artist_name == '':
            yield None
        
        else:
            yield {
            'title': title,
            'item_url': response.url,
            'artist_name': artist_name,
            'author': author,
            'img': img,
            'publication_datetime': publication_datetime,
            'wiki_link': wiki_link,
            'spotify_link': spotify_link,
            'spotify_about': spotify_about,
            }
    


        
















































        

    
