import logging, sys
import requests

class RecipescraperPipeline(object):
    def process_item(self, item, spider):
        for ingredient in item['ingredients']:
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

            # Todo: retrieve the UUID from the response body.
            ingredient_uuid = response.json()['data']['id']

        return item
