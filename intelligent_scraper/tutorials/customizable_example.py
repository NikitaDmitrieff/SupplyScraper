import os
from crawl4ai import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from config import setup_api_keys_and_langsmith

setup_api_keys_and_langsmith(
    langsmith_tracking=True, project_name="intelligent_scraper_tests"
)


class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(
        ..., description="Fee for output token ßfor the OpenAI model."
    )


url = "https://openai.com/api/pricing/"
crawler = WebCrawler()
crawler.warmup()

result = crawler.run(
    url=url,
    word_count_threshold=1,
    extraction_strategy=LLMExtractionStrategy(
        provider="openai/gpt-4o-mini",
        api_token=os.getenv("OPENAI_API_KEY"),
        schema=OpenAIModelFee.schema(),
        extraction_type="schema",
        instruction="""From the crawled content, extract all mentioned model names along with their fees for input and output tokens. 
            Do not miss any models in the entire content. One extracted model JSON format should look like this: 
            {"model_name": "GPT-4", "input_fee": "US$10.00 / 1M tokens", "output_fee": "US$30.00 / 1M tokens"}.""",
    ),
    bypass_cache=True,
)

print(result.extracted_content)
