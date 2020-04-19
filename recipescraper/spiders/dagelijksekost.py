import scrapy


class DagelijksekostSpider(scrapy.Spider):
    name = 'dagelijksekost'
    allowed_domains = ['dagelijksekost.een.be']
    start_urls = ['https://dagelijksekost.een.be/az-index']

    def parse(self, response):
        recipes = []
        for data in response.css('ul.az-letter__links li'):
            recipes.append('\n'.join([
                data.css('a::text').extract_first(),
                'https://dagelijksekost.een.be' + data.xpath('.//a/@href').extract_first(),
            ]))

        filename = 'recipes.txt'
        with open(filename, 'w') as f:
            f.write('\n\n'.join(recipes))
