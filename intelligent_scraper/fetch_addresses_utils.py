import os
from typing import List

import requests

from base_model import BaseModel
from intelligent_scraper.config import setup_google_api_key
import time
from prompts import format_select_type_filters_prompt
import json

setup_google_api_key()


class ProductCategoryMapper(BaseModel):
    def map_product_to_category(self, product_query: str) -> List[str]:

        prompt = format_select_type_filters_prompt(query=product_query)
        category, _, _ = self.generate_answer(user_prompt=prompt)

        try:
            selected_filters = json.loads(category)
            return selected_filters
        except json.JSONDecodeError:
            breakpoint()
            return [category]


def get_all_shops_in_area(
    api_key: str,
    latitude: float,
    longitude: float,
    radius: int = 1500,
    type_filters: List[str] = None,
    number_of_shops_to_gather: int = 20,
) -> List:

    if type_filters is None:
        type_filters = ["store"]

    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    all_shops = []

    for type_filter in type_filters:

        params = {
            "key": api_key,
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "type": type_filter,
        }

        while True or len(all_shops) > number_of_shops_to_gather:
            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                return all_shops

            data = response.json()
            all_shops.extend(data.get("results", []))

            # handle next page
            next_page_token = data.get("next_page_token")
            if not next_page_token:
                break  # No more pages

            params["pagetoken"] = next_page_token
            time.sleep(2)

    return all_shops


def get_shop_details(api_key: str, place_id: str) -> dict:
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "key": api_key,
        "place_id": place_id,
        "fields": "name,rating,formatted_phone_number,formatted_address,website",
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json().get("result", {})
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


# Example usage:
if __name__ == "__main__":
    api_key = os.getenv("GOOGLE_API_KEY")
    latitude = 48.8566  # Latitude for Paris
    longitude = 2.3522  # Longitude for Paris
    radius = 500  # Search radius in meters

    categories = ProductCategoryMapper().map_product_to_category(
        product_query="a green big dinosor"
    )

    print(categories)

    shops = get_all_shops_in_area(
        api_key, latitude, longitude, radius, type_filters=categories
    )

    for index, shop in enumerate(shops):
        if index > 100:
            break
        else:
            shop_details = get_shop_details(api_key, shop["place_id"])
            shop_address = shop_details.get("website", "None")
            print(shop_details.get("name", "no name"), shop_address)
