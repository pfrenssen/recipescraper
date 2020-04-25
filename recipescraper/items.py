import scrapy


# Model for a recipe.
class RecipeItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    cuisine = scrapy.Field()
    diet = scrapy.Field()
    ingredients = scrapy.Field()
    keywords = scrapy.Field()
    time = scrapy.Field()
