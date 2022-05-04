"""
Crawl all data in website: chinadaily.com.cn
"""

import scrapy
import time
import json
from Webpage_Crawler.items import WebpageCrawlerItem

class Crawler1Spider(scrapy.Spider):
    name = 'crawler1'
    allowed_domains = ['chinadaily.com.cn']
    custom_settings = {'LOG_LEVEL': 'ERROR'}

    max_pages = 400
    urls = []
    count = 0

    def gen_urls(self, genre, topics):
        """
        Generate all the urls that we need.
        """
        for topic in topics:
            for i in range(1, self.max_pages):
                url = f'https://www.chinadaily.com.cn/{genre}/{topic}/page_{i}.html'
                self.urls.append(url)

    def start_requests(self):
        sports_topics = ['soccer', 'basketball', 'volleyball', 'tennis', 
                         'golf', '59b8d012a3108c54ed7dfc72', 'swimming', 'china']
        
        china_topics = ['governmentandpolicy', 'society', 'scitech', '59b8d010a3108c54ed7dfc30'
                        'coverstory', 'environment', '59b8d010a3108c54ed7dfc27', '59b8d010a3108c54ed7dfc25']
        
        world_topics = ['asia_pacific', 'america', 'europe', 'middle_east',
                        'africa', 'china-us', 'cn_eu', 'China-Japan-Relations', 'china-africa']
        
        business_topics = ['economy', 'companies', 'biz_industries', 'tech', 'motoring', 
                           'money']

        lifestyle_topics = ['fashion', 'celebrity', 'people', 'food', 
                            'health', 'video', 'photo']
        
        culture_topics = ['art', 'musicandtheater', 'filmandtv', 'books', 
                          'heritage', 'eventandfestival', 'culturalexchange']
        
        travel_topics = ['news', 'citytours', 'guidesandtips', 'footprint', 
                         'aroundworld', '59b8d013a3108c54ed7dfca3', 'photo', 'video']
        
        opinion_topics = ['editionals', 'op-ed', 'commentator', 'opinionline']

        self.gen_urls('sports', sports_topics)
        self.gen_urls('china', china_topics)
        self.gen_urls('world', world_topics)
        self.gen_urls('business', business_topics)
        self.gen_urls('life', lifestyle_topics)
        self.gen_urls('culture', culture_topics)
        self.gen_urls('travel', travel_topics)
        self.gen_urls('opinion', opinion_topics)

        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        detail_urls = []
        parent_nodes = response.xpath('//span[@class="tw3_01_2_t"]')
        p_contents = parent_nodes.getall()
        if len(p_contents) != 0:
            print(f'Crawling the url: [{response.url}')
            for node in parent_nodes:
                url = node.xpath('h4/a/@href').get()
                detail_urls.append(f'https:{url}')
            
            for url in detail_urls:
                yield scrapy.Request(url, callback=self.get_item)
        else:
            print(f'No target contents in url: [{response.url}]')
    
    def parse_detail(self, response):
        """
        This method will directly save data into a csv file.
        """
        page_url = str(response.url)
        page_title = response.xpath('//h1/text()').get()      # Only one title in a article
        page_content = response.xpath('//div[@id="Content"]/p/text()').getall()  # Contents are seperated into many paragraphs

        if (page_title is not None) and (len(page_content) != 0):
            page_title = page_title.strip()
            page_content = ' '.join(page_content)
            page_content = page_content.strip()
            with open('chinadaily1.csv', 'a', encoding='utf-8') as f:
                f.write(page_url + '\t' + page_title + '\t' + page_content)
                f.write('\n')
        else:
            print(f'No target contents in url: [{response.url}]')
    
    def get_item(self, response):
        """
        This method will return a new item to pipelines, then pipelines will do the job.
        """
        page_url = str(response.url)
        page_title = response.xpath('//h1/text()').get()                         # Only one title in a article
        page_content = response.xpath('//div[@id="Content"]/p/text()').getall()  # Contents are seperated into many paragraphs, so page_content is a list object

        item = WebpageCrawlerItem()

        if (page_title is not None) and (len(page_content) != 0):
            page_title = page_title.strip()
            page_content = '\n'.join(page_content)
            page_content = page_content.strip()
            item['id'] = self.count
            item['url'] = page_url
            item['title'] = page_title
            item['content'] = page_content
            self.count += 1
            return item
        else:
            print(f'No target contents in url: [{response.url}]')