import json
from typing import List
from crawl4ai import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from intelligent_scraper.crawler_utils import Product, json_to_csv
import os


class ShopInventoryScraper:
    def __init__(
        self, base_url: str, nearby_shops_urls: List[str], crawler: WebCrawler = None
    ):
        self.base_url = base_url
        self.nearby_shops_urls = nearby_shops_urls
        self.crawler = crawler if crawler else WebCrawler()
        self.crawler.warmup()

    def scrape_inventory(self) -> List[Product]:
        all_products = []
        for shop_url in self.nearby_shops_urls:
            full_url = f"{self.base_url}{shop_url}"
            result = self._scrape_single_shop(full_url)
            if result:
                all_products.extend(result)
        return all_products

    def _scrape_single_shop(self, url: str) -> List[Product]:
        extraction_strategy = LLMExtractionStrategy(
            provider="openai/gpt-4o-mini",
            api_token=os.getenv("OPENAI_API_KEY"),
            schema=Product.schema(),
            extraction_type="schema",
            instruction="""Extract all products available along with their prices from the given shop's webpage. 
                           Each extracted product should have a name and price in the following JSON format: 
                           {"product_name": "Item Name", "product_price": "Price"}""",
        )
        result = self.crawler.run(
            url=url,
            word_count_threshold=1,
            extraction_strategy=extraction_strategy,
            bypass_cache=True,
        )

        result = json.loads(result.dict()["extracted_content"])

        return [Product(**item) for item in result] if result else []

    def save_inventory_to_csv(self, output_csv: str):
        all_products = self.scrape_inventory()
        products_json = json.dumps([product.dict() for product in all_products])
        json_to_csv(products_json, output_csv)


if __name__ == "__main__":
    # Usage Example:
    base_url = "https://www.decathlon.fr"
    nearby_shops = ["/homme/polos"]  # , "/femme/chaussures", "/enfant/maillots"
    scraper = ShopInventoryScraper(base_url=base_url, nearby_shops_urls=nearby_shops)
    scraper.save_inventory_to_csv("nearby_shops_inventory.csv")
