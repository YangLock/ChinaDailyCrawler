# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import json

class WebpageCrawlerPipeline_csv:
    def __init__(self):
        self.f = open('chinadaily2.csv', 'w', newline='')
        self.csvwriter = csv.writer(self.f, delimiter='\t')
        self.csvwriter.writerow(['page_url', 'page_title', 'page_content'])

    def process_item(self, item, spider):
        self.csvwriter.writerow([item['url'], item['title'], item['content']])
        return item

    def close_spider(self, spider):
        self.f.close()
    
class WebpageCrawlerPipeline_json:
    def __init__(self):
        self.f = open('chinadaily.json', 'w')
    
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        self.f.write(content)
        self.f.write('\n')
        return item
    
    def close_spider(self, spider):
        self.f.close()
