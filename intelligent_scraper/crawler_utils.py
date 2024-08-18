from BaseModel.base_model import BaseModel
import os
from crawl4ai import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel as BM, Field
from config import setup_api_keys_and_langsmith
import json
import pandas as pd

setup_api_keys_and_langsmith(
    langsmith_tracking=True, project_name="intelligent_scraper_tests"
)


class Product(BM):
    product_name: str = Field(..., description="Name of the product")
    product_price: str = Field(..., description="Price of the product")


def json_to_csv(json_data: str, output_csv: str):
    # Convert the JSON data to a list of dictionaries
    try:
        # If the JSON data is in a single string with newline escape characters
        clean_json_data = (
            json_data.replace("\\n", "").replace("\\", "").replace("u20ac", "€")
        )
        data = json.loads(clean_json_data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv(output_csv, index=False)
    print(f"Data successfully saved to {output_csv}")


def scrape_one_page(
    url: str = "https://openai.com/api/pricing/", crawler: WebCrawler = None
):

    if not crawler:
        crawler = WebCrawler()
        crawler.warmup()

    result = crawler.run(
        url=url,
        word_count_threshold=1,
        extraction_strategy=LLMExtractionStrategy(
            provider="openai/gpt-4o-mini",
            api_token=os.getenv("OPENAI_API_KEY"),
            schema=Product.schema(),
            extraction_type="schema",
            instruction="""From the crawled content, extract all products available along with their prices. 
                One extracted product JSON format should look like this: 
                {"product_name": "Umbrella", "product_price": "US$10.00"}""",
        ),
        bypass_cache=True,
    )
    return result


def quick_talk(question: str = "How are you?"):
    generator = BaseModel()
    answer, sys_prompt, user_prompt = generator.generate_answer(user_question=question)
    print(answer)


print(scrape_one_page(url="https://www.decathlon.fr/homme/polos"))
