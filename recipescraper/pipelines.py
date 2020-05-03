import logging, sys
import requests
from scrapy.exceptions import DropItem


# Publishes the scraped content to a JSON:API server.
class JsonApiPipeline(object):

    def __init__(self):
        self.ingredients = {}

    def process_item(self, item, spider):
        ingredient_ids = []

        # In order to post the recipe to JSON:API we need the UUIDs of the ingredients. We will retrieve these from the
        # server. In case the ingredient doesn't exist yet on the server we will create it.
        for ingredient in item['ingredients']:
            # Request the ID for this ingredient from the server.
            ingredient_id = self.get_ingredient_id(ingredient)
            if not ingredient_id:
                # Ingredient doesn't exist on the server, create it.
                ingredient_id = self.create_ingredient(ingredient)

            # Compile a list of ingredient IDs in the format expected by the REST API.
            ingredient_ids.append({
                "type": "ingredient--ingredient",
                "id": ingredient_id,
            })

        recipe_data = {
            "data": {
                "type": "recipe--recipe",
                "attributes": {
                    "title": item['title'][0],
                    "field_project": item['project'][0],
                    "field_spider": item['spider'][0],
                    "field_instance": item['instance'][0],
                    "field_url": item['url'][0]
                },
                "relationships": {
                    "field_ingredients": {
                        "data": ingredient_ids
                    }
                }
            }
        }

        response = requests.post(
            'http://recipefinder.local/jsonapi/recipe/recipe',
            json=recipe_data,
            headers={
                "Accept": "application/vnd.api+json",
                "Content-type": "application/vnd.api+json",
            },
            auth=("admin", "admin")
        )

        if response.status_code != 201:
            logging.warning("response code %s", response.status_code)
            logging.warning("response: %r", response.json())
            raise DropItem("Could not store recipe '%s'" % item['title'][0])

        return item

    def create_ingredient(self, ingredient):
        ingredient_data = {
            "data": {
                "type": "ingredient--ingredient",
                "attributes": {
                    "title": ingredient
                }
            }
        }

        response = requests.post(
            'http://recipefinder.local/jsonapi/ingredient/ingredient',
            json=ingredient_data,
            headers={
                "Accept": "application/vnd.api+json",
                "Content-type": "application/vnd.api+json",
            },
            auth=("admin", "admin")
        )

        if response.status_code != 201:
            raise DropItem("Could not store ingredient '%s'." % ingredient)

        ingredient_id = response.json()['data']['id']
        self.ingredients[ingredient] = ingredient_id

        return ingredient_id

    def get_ingredient_id(self, ingredient):
        if ingredient in self.ingredients:
            logging.debug('Using cached UUID %s for %s', self.ingredients[ingredient], ingredient)
            return self.ingredients[ingredient]

        params = {
            "filter[title][condition][path]": "title",
            "filter[title][condition][operator]": "=",
            "filter[title][condition][value]": ingredient
        }
        response = requests.get(
            'http://recipefinder.local/jsonapi/ingredient/ingredient',
            params=params,
            headers={
                "Accept": "application/vnd.api+json",
            },
            auth=("admin", "admin")
        )

        if response.status_code != 200:
            raise DropItem("UUID could not be retrieved for '%s'" % ingredient)

        response_data = response.json()['data']
        for data in response_data:
            # Return the first match.
            if 'id' in data:
                ingredient_id = data['id']
                self.ingredients[ingredient] = ingredient_id
                logging.debug("Retrieved UUID %s for '%s'", self.ingredients[ingredient], ingredient)
                return ingredient_id

        return None
