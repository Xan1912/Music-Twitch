import scrapy
import re

import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

class RollingstonesSpider(scrapy.Spider):
    name = 'rollingstones'
    allowed_domains = ['rollingstones.com']
    start_urls = ['https://www.rollingstone.com/music/']

    def parse(self, response):
        
        #Extracting the content using xpath selectors
        
        titles = [response.xpath('//div[@class="l-blog__item l-blog__item--spacer-s"]/ul/li[{}]/article/a/header/h3/text()'.format(i)).extract() for i in range(1,30)]
        link = response.xpath('//*[@id="site_wrap"]/div[3]/div[1]/main/div[3]/ul/li[1]/article/a/@href').extract()
        category = response.xpath('//*[@id="site_wrap"]/div[3]/div[1]/main/div[3]/ul/li[1]/article/a/header/div[1]/span[2]/text()').extract()
        img = response.xpath('//*[@id="site_wrap"]/div[3]/div[1]/main/div[3]/ul/li[1]/article/a/figure/div/img/@src').extract()
        
        # Setting the regex parser for names 

        reg_name = r'[A-Z]([a-z]+|\.)(?:\s+[A-Z]([a-z]+|\.))*(?:\s+[a-z][a-z\-]+){0,2}\s+[A-Z]([a-z]+|\.)'

        # Extract and store names

        # Here the code will be redirected towards the inner page and from their we shall make queries to the reddit
        # And the Wiki page to derive more information. Further plans to make requests to Twitter(if time permits) and Spotify API and get the 
        # most relevant Tweets and the most relevant songs of the artist : Contribute more to the music encyclopedia

        # Authenticating the API with the required credentials 
        client_credentials_manager = SpotifyClientCredentials(client_id='b7cf2f5f0e074d1ca984a546822797cc',
                                client_secret='c435b02f49304b7db74ec08ddb7df6e7')
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Example Query
        name = 'Radiohead'
        results = spotify.search(q='artist:' + name, type='artist')
        items = results['artists']['items']

        # Give the extracted content row wise
        for item in zip(titles,link,category,img):
            
            #create a dictionary to store the scraped info
            if item[0] != []:
                scraped_info = {
                    'title' : "".join(item[0]).replace('\n','').replace('\t',''),                
                    'link' : item[1],
                    'category' : item[2],
                    'img' : item[3]
                }

                # Provide the scraped info to scrapy
        
                yield scraped_info

        # Redirections to the next page
        
        next_page = response.xpath('//*[@id="site_wrap"]/div[3]/div[1]/main/div[4]/div/a[2]/@href').extract()
        
        # Double check if next_page is not empty
        
        if next_page == []: 
            next_page = response.xpath('//*[@id="site_wrap"]/div[3]/div[1]/main/div[4]/div/a[1]/@href').extract()
        
        # Assign the URL to the next page to start the crawl again

        if next_page:
            next_href = next_page[0]
            next_page_url = next_href
            request = scrapy.Request(url=next_page_url)
            yield request
