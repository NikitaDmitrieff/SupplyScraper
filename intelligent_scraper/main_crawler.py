import csv
import json
from typing import List

from intelligent_scraper.fetch_addresses_utils import query_a_product
from intelligent_scraper.fetch_products import ShopInventoryScraper
from intelligent_scraper.fetch_products_utils import json_to_csv


def retrieve_websites(csv_file_path: str) -> List:
    websites = []

    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            website = row.get("Website")
            if website and website.lower() != "no website":
                websites.append(website)

    return websites


def retrieve_products_with_keyword(csv_file_path: str, keyword: str) -> List:
    matching_rows = []

    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (
                keyword.lower() in row["product_name"].lower()
                or keyword.lower() in row["product_description"].lower()
            ):
                matching_rows.append(row)

    return matching_rows


if __name__ == "__main__":
    max_website_search = 10
    shops_csv_name = "scrapped_shops.csv"

    query_a_product(product="iphone", output_filename=shops_csv_name)
    websites = retrieve_websites(shops_csv_name)

    product_list = []

    for website in websites[: min(len(websites), max_website_search)]:
        nearby_shops = [""]
        scraper = ShopInventoryScraper(base_url=website, nearby_shops_urls=nearby_shops)
        products = scraper.scrape_inventory()
        product_list.extend(products)

    products_json = json.dumps([product.dict() for product in product_list])
    json_to_csv(products_json, "nearby_shops_inventory.csv")

    matching_rows = retrieve_products_with_keyword(
        "nearby_shops_inventory.csv", "iphone"
    )

    print(matching_rows)
