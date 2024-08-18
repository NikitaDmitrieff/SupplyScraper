from typing import List

from base_model import BaseModel


class ShopWebsiteRetriever(BaseModel):
    def get_shop_websites(self, location: str) -> List[str]:
        # Formulate the query to ask ChatGPT
        query = f"List all shop websites in {location}."

        # Generate answer using the existing method
        answer, system_prompt, user_prompt = self.generate_answer(user_question=query)

        # Optional: Parse the response to extract shop websites (depends on the response format)
        shop_websites = self.parse_shop_websites(answer)

        return shop_websites

    def parse_shop_websites(self, response: str) -> List[str]:
        # Assuming the response contains URLs, you can extract them using regex or similar logic.
        import re

        # Simple regex to find URLs
        url_pattern = re.compile(r"https?://\S+")
        websites = url_pattern.findall(response)

        return websites


if __name__ == "__main__":
    chat = ShopWebsiteRetriever()

    location = "Paris"
    shop_websites = chat.get_shop_websites(location=location)

    print(f"Shop websites in {location}:")
    for website in shop_websites:
        print(website)
