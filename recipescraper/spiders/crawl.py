import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from recipescraper.items import RecipeItem


class CrawlySpider(CrawlSpider):
    name = 'crawl'
    allowed_domains = ['dagelijksekost.een.be']
    start_urls = ['https://dagelijksekost.een.be/az-index']

    rules = (
        Rule(LinkExtractor(allow=r'^https://dagelijksekost.een.be/gerechten/'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        l = ItemLoader(item=RecipeItem(), response=response)
        l.add_xpath('title', '(//h1)[1]/text()')
        l.add_xpath('image', '//meta[@property = "og:image"]/@content')

        return l.load_item()
