import scrapy
from scrapy_interview.items import ChainItem
from scrapy import Request

class LinkSpiderSpider(scrapy.Spider):
    name = "link_spider"
    allowed_domains = ["locations.oreillyauto.com"]
    start_urls = ["https://locations.oreillyauto.com/"]

    scrape_type = "html - multi-page"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }

    def parse(self, response):
        states = response.xpath('//a[@class="ga-link map-list-link"]')
        for state in states[:1]:  # ← this limits it to just the first 2 states
            state_link = state.xpath('./@href').get()
            print("State Link:", state_link)
            yield response.follow(state_link, callback=self.parse_city, headers=self.headers)

    def parse_city(self, response):
        cities = response.xpath('//a[@class="ga-link map-list-link"]')
        for city in cities:
            city_link = city.xpath('./@href').get()
            print("City Link:", city_link)
            yield response.follow(city_link, callback=self.parse_store_list, headers=self.headers)

    def parse_store_list(self, response):
        stores = response.css('.map-list-content')
        print(stores)
        for store in stores:
            print("Priyanka")
            store_link = store.xpath('./@href').get()
            print("Store Link:", store_link)
            yield response.follow(store_link, callback=self.parse_store, headers=self.headers)

    def parse_store(self, response):
        store_data=response.xpath('//*[@class="details-wrap"]')
        for data in store_data:
            item = ChainItem()
            item["store_name"] = data.xpath('//h1/text()').get()
            print("Store Name:", item["store_name"])
            item["address"] = data.xpath('//div[@class="c-address-street-1"]/text()').get()
            item["city"] = data.xpath('//span[@class="c-address-city"]/text()').get()
            item["state"] = data.xpath('//abbr[@class="c-address-state"]/text()').get()
            item["zip_code"] = data.xpath('//span[@class="c-address-postal-code"]/text()').get()
            item["phone_number"] = data.xpath('//div[contains(@class, "c-phone-number")]/text()').get()

            # Optional fields for ChainItem compatibility
            item["store_number"] = ""
            item["store_type"] = ""
            item["latitude"] = ""
            item["longitude"] = ""
            item["store_hours"] = ""
            item["other_fields"] = ""
            item["coming_soon"] = ""
            item["attributes"] = {
                "DRIVETHRU": ""
            }
            print("🟢 Reached store page:", response.url)
            yield item
