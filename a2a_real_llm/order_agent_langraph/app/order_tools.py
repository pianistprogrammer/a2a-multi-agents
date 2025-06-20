import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from dummy_data import COMBINED_DATA

from pydantic import BaseModel, Field
from langchain_core.tools import tool
import logging

class OrderLookupInput(BaseModel):
    order_id: str = Field(..., description="The order ID to check")

@tool(args_schema=OrderLookupInput)
def get_order_status(order_id: str) -> str:
    """Retrieve order status and tracking details with enriched product info."""
    if not order_id or not order_id.strip():
        return "❗ You must provide a valid order ID."

    order_id = order_id.strip().upper()
    logging.info(f"Looking up order status for order ID: {order_id}")
    order = COMBINED_DATA["ORDER_DATABASE"].get(order_id)

    if not order:
        return f"❌ No order found with ID `{order_id}`."

    # Build item details
    item_lines = []
    for item in order["items"]:
        product_id = item["product_id"]
        quantity = item["quantity"]
        product = COMBINED_DATA["PRODUCT_CATALOG"].get(product_id)

        if product:
            item_lines.append(
                f"- {product['name']} (x{quantity}) - ${product['price']:.2f} each"
            )
        else:
            item_lines.append(f"- Unknown product ID `{product_id}` (x{quantity})")

    message = f"""📦 **Order `{order_id}` Details**
        - **Status:** {order['status']}
        - **Order Date:** {order['order_date']}
        - **Total Amount:** ${order['total_amount']:.2f}
        - **Items Ordered:**
        {chr(10).join(item_lines)}"""

    if order["status"].lower() == "shipped":
        message += f"""
        - **Carrier:** {order['carrier']}
        - **Tracking Number:** {order['tracking_number']}
        - **Expected Delivery:** {order['expected_delivery']}"""

    return message
