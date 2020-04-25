import json
import re
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

        # Retrieve the ingredients from structured JS data in the page.
        js_script = response.xpath('//*[@class="content-container"]//script').get()
        if js_script:
            ingredients_json = re.search('var ingredients = (.*);', js_script).group(1)
            if ingredients_json:
                ingredients = []
                for ingredient in json.loads(ingredients_json):
                    product_name = ingredient['product']['name']
                    ingredients.append(product_name)
                l.add_value('ingredients', ",".join(ingredients))

        return l.load_item()
