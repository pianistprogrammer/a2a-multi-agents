from typing import Any, Dict
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from dummy_data import COMBINED_DATA  # or PRODUCT_CATALOG if you renamed it

def get_product_info(product_id: str) -> Dict[str, Any]:
    product = COMBINED_DATA["PRODUCT_CATALOG"].get(product_id)
    if not product:
        return {"success": False, "error": f"Product with ID '{product_id}' not found."}
    
    return {
        "success": True,
        "data": {
            "id": product_id,
            "name": product["name"],
            "description": product["description"],
            "price": product["price"],
            "specs": product["specs"],
        }
    }


def check_stock(product_id: str) -> Dict[str, Any]:
    product = COMBINED_DATA["PRODUCT_CATALOG"].get(product_id)
    if not product:
        return {"success": False, "error": f"Product with ID '{product_id}' not found."}
    
    return {
        "success": True,
        "data": {
            "id": product_id,
            "stock": product["stock"]
        }
    }


def summarize_reviews(product_id: str) -> str:
    product = COMBINED_DATA["PRODUCT_CATALOG"].get(product_id)
    if not product or not product.get("reviews"):
        return "No reviews available."

    reviews = product["reviews"]
    count = len(reviews)
    top_reviews = ", ".join(reviews[:2])

    return (
        f"{count} reviews: {top_reviews}, and more..."
        if count > 2 else
        f"{count} reviews: {top_reviews}"
    )


agent = LlmAgent(
    name="ProductInformationAgent",
    description="Provides detailed product info, stock status, and customer review summaries.",
    model=LiteLlm(
        api_base="http://localhost:11434/v1",
        model="openai/qwen3:1.7b",
        api_key="ollama",
    ),
    tools=[get_product_info, check_stock, summarize_reviews],
    instruction="""
    You are a product assistant who helps customers with detailed product info.

    ## Tasks:
    - Use `get_product_info` to retrieve full details of a product.
    - Use `check_stock` to get how many units are available.
    - Use `summarize_reviews` to give a quick overview of customer sentiment.

    ## Example Workflow:
    1. If asked "Tell me about P002", call `get_product_info("P002")`.
    2. If asked "Is it in stock?", call `check_stock("P002")`.
    3. For reviews, call `summarize_reviews("P002")`.

    Always respond using the tools provided.
    Do not guess product details or stock levels.
    """,
)


def create_agent() -> LlmAgent:
    return agent
