import json
from datetime import datetime
import xml.etree.ElementTree as ET
import requests
import asyncio
import aiohttp
import math
import logging
import random

class WPXmlSitemapGenerator:
    def __init__(self,config,config_file=None):
        self.config = config
        if isinstance(config_file,str):
            self.config = json.load(open(config_file))
        self.headers = {'User-Agent': 'My User Agent 1.0'}
        self.responses = []
        # Configure asynchronous logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    def start(self):
        response1 = requests.get(self.config.get("full_url")+"?rest_route=/wp/v2/posts/",headers=self.headers)
        print("\n\nResponse Headers:\n\n")
        print(response1.headers)
        assert(response1.headers['x-wp-total'])
        print("Total Post => "+response1.headers['x-wp-total'])
        urls = self.get_urls_from_wp_total(response1.headers['x-wp-total'])
        self.start_request(urls)

    def generate_xml(self, json_response):
        print("Total Crawled Links => "+str(len(json_response)))
        print("Total Crawled Items => "+str(len(json_response)*len(json_response[0])))
        root = ET.Element("urlset",xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        assert(json_response[0])
        for items in json_response:
           for item in items:
              print(item['link'])
              print(item['modified']+"\n")
              doc = ET.SubElement(root, "url")
              ET.SubElement(doc, "loc").text = item['link']
              ET.SubElement(doc, "lastmod").text = item['modified'] if self.config.get("url_set_config").get('date_val') else self.get_time_now()
              ET.SubElement(doc, "priority").text = "1" if not self.config.get("url_set_config").get('priority_val') else self.get_random_priority()

           tree = ET.ElementTree(root)
           ET.indent(tree, space='  ', level=0)
           tree.write(self.config.get("output_file"),encoding='utf-8',xml_declaration=True)

    def start_request(self,urls):
        loop = asyncio.get_event_loop()
        full_json_responses = loop.run_until_complete(self.make_requests(urls))
        self.generate_xml(full_json_responses)

    async def fetch(self, session, url):
       async with session.get(url) as response:
          return await response.json()

    async def make_requests(self, urls):
       async with aiohttp.ClientSession() as session:
          tasks = []
          for url in urls:
             tasks.append(asyncio.create_task(self.fetch(session, url)))
          for task in asyncio.as_completed(tasks):
             response = await task
             self.logger.info("Parsed: "+str(len(response)))  # 
             self.responses.append(response)
       return self.responses

    def get_urls_from_wp_total(self,wp_total):
         base_url = self.config.get("full_url")+"?rest_route=/wp/v2/posts/"
         per_page = 100
         total_pages = int(wp_total)
         group_pages = int(math.ceil(total_pages / per_page))
         final_urls = []
         for page in range(1,group_pages+1):
             url = f"{base_url}&page={page}&per_page={per_page}"
             final_urls.append(url)
         print("\nGenerated urls:\n"+str(len(final_urls)))
         return final_urls

    def get_time_now(self):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        return formatted_datetime
    
    def get_random_priority(self):
        random_float = random.uniform(0.1, 1.0)
        rounded_float = round(random_float, 1)
        return str(rounded_float)

