from typing import Iterable
import scrapy
from scrapy.http import Request
from auto.spiders.autogidas_utils.autogidas_helper import autogidas_helper



class AutogidasSpider(scrapy.Spider):
    name = "autogidas"
    allowed_domains = ["autogidas.lt"]
    start_urls = ["https://autogidas.lt/skelbimai/automobiliai/?f_50=kaina_asc&page=1"]
    helper = autogidas_helper()

    def start_requests(self):
        
        
        return super().start_requests()

    def parse(self, response):
        total_pages = response.xpath(f"(//div[@class='page last']/parent::a/preceding-sibling::*)[last()]/div/text()").get()
        current_page = response.url.split("=")[-1]
        car_list = self.helper.extract_cars_from_search_page(response)
        
        for car in car_list:
            yield car
        
        if int(current_page) < int(total_pages):
            next_page = int(current_page) + 1
            url = f"https://autogidas.lt/skelbimai/automobiliai/?f_50=kaina_asc&page={next_page}"
            yield scrapy.Request(url=url, callback=self.parse)