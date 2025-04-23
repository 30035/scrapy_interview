from contextlib import nullcontext

import scrapy

from scrapy_interview.items import ChainItem
from scrapy import Request
class PracticeSpiderSpider(scrapy.Spider):
    name = "practice_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    scrape_type = "html - single-page"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }


    def parse(self, response):
     books=response.xpath('//*[@class="product_pod"]')
     for book in books:
         item=ChainItem()
         item["store_name"]=''.join(book.css(
        'a::text'
         ).extract_first()).strip()
         item["address"]=book.css(
        '.thumbnail::attr(src)'
         ).extract_first().strip()
         item["phone_number"] = book.css(
        '.price_color::text'
         ).extract_first().strip()
         item["store_number"] = ""
         item["store_type"] = ""
         item["address2"] = ""
         item["city"] = ""
         item["state"] = ""
         item["zip_code"] = ""
         item["country"] = ""
         item["latitude"] = ""
         item["longitude"] = ""
         item["store_hours"] = ""
         item["other_fields"] = ""
         item["coming_soon"] = ""
         item["attributes"] = {"DRIVETHRU": ""}
         yield item


     next_page=response.xpath('.//li[@class="next"]/a/@href').get()
     if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

