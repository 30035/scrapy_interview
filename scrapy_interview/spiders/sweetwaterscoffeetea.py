# -*- coding: utf-8 -*-
# AUTHOR: Unknown
import scrapy
import json
from scrapy_interview.items import ChainItem
from scrapy import Request
import scrapy_interview.utils as utils

class SweetwaterscoffeeteaSpider(scrapy.Spider):
    name = "sweetwaterscoffeetea"
    #valid scrape_type values: html - single-page, html - multi-page, json - single-page, kml, selenium, other
    scrape_type = "html - single-page"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }

    def start_requests(self):
        url = "https://www.sweetwaterscafe.com/locations/"
        yield Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        stores = response.xpath('//*[@class="location-card-wrapper"]//li')
        for store in stores:
            item = ChainItem()
            item["store_name"] = store.xpath(
                './/h2[@class="nomargin"]//text()'
            ).extract_first()
            item["store_number"] = ""
            item["store_type"] = ""
            item["address"] = store.xpath(
                './/*[@itemprop="streetAddress"]//text()'
            ).extract_first()
            item["address2"] = ""
            item["city"] = store.xpath(
                './/*[@itemprop="addressLocality"]//text()'
            ).extract_first()
            item["state"] = store.xpath(
                './/*[@itemprop="addressRegion"]//text()'
            ).extract_first()
            item["zip_code"] = store.xpath(
                './/*[@itemprop="postalCode"]//text()'
            ).extract_first()
            item["country"] = "USA"
            item["phone_number"] = store.xpath(
                './/*[@itemprop="telephone"]//text()'
            ).extract_first()
            item["latitude"] = ""
            item["longitude"] = ""
            item["store_hours"] = ""
            item["other_fields"] = ""
            item["coming_soon"] = ""
            item["attributes"] = {
                "DRIVETHRU":""
            }

            yield item
