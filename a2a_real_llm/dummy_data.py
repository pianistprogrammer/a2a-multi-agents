COMBINED_DATA = {
    # --- Product Data ---
    "PRODUCT_CATALOG": {
        "P001": {
            "name": "Wireless Mouse",
            "description": "Ergonomic wireless mouse with USB receiver.",
            "price": 25.99,
            "specs": {"connectivity": "2.4GHz", "battery": "AA", "dpi": "1600"},
            "stock": 15,
            "reviews": ["Works great!", "Good value for money", "Battery life is short."],
        },
        "P002": {
            "name": "Mechanical Keyboard",
            "description": "RGB mechanical keyboard with blue switches.",
            "price": 59.99,
            "specs": {"switch_type": "Blue", "layout": "ANSI", "backlight": "RGB"},
            "stock": 8,
            "reviews": ["Clicky and responsive", "Loud but satisfying", "Great for typing"],
        },
        "P003": {
            "name": "27-inch Monitor",
            "description": "1080p Full HD monitor with HDMI and VGA input.",
            "price": 179.99,
            "specs": {"resolution": "1920x1080", "refresh_rate": "75Hz", "panel": "IPS"},
            "stock": 5,
            "reviews": ["Crisp display", "Great for the price", "Average build quality"],
        },
        "P004": {
            "name": "USB-C Hub",
            "description": "Multi-port USB-C hub with HDMI, USB-A, and SD card.",
            "price": 39.99,
            "specs": {"ports": "HDMI, 3x USB-A, SD, MicroSD", "power": "Pass-through"},
            "stock": 22,
            "reviews": ["Perfect for MacBook", "Gets warm sometimes", "Very convenient"],
        },
        "P005": {
            "name": "Laptop Stand",
            "description": "Adjustable aluminum laptop stand for desks.",
            "price": 29.99,
            "specs": {"material": "Aluminum", "adjustable": "Yes"},
            "stock": 30,
            "reviews": ["Solid build", "Easy to adjust", "Too heavy for travel"],
        },
        "P006": {
            "name": "Bluetooth Speaker",
            "description": "Portable Bluetooth speaker with deep bass.",
            "price": 49.99,
            "specs": {"battery": "10h", "waterproof": "Yes", "range": "30ft"},
            "stock": 12,
            "reviews": ["Loud and clear", "Bass is amazing", "Battery could last longer"],
        },
        "P007": {
            "name": "Noise Cancelling Headphones",
            "description": "Over-ear headphones with active noise cancellation.",
            "price": 99.99,
            "specs": {"ANC": "Yes", "battery": "20h", "connection": "Bluetooth"},
            "stock": 9,
            "reviews": ["Blocks noise well", "Comfortable", "Slightly bulky"],
        },
        "P008": {
            "name": "4K Webcam",
            "description": "USB 4K webcam with built-in microphone.",
            "price": 89.99,
            "specs": {"resolution": "4K", "microphone": "Built-in", "connection": "USB"},
            "stock": 10,
            "reviews": ["Sharp video", "Plug and play", "Poor low light"],
        },
        "P009": {
            "name": "External SSD 1TB",
            "description": "High-speed USB-C external SSD drive.",
            "price": 129.99,
            "specs": {"capacity": "1TB", "speed": "Up to 1000MB/s", "connection": "USB-C"},
            "stock": 18,
            "reviews": ["Very fast", "Compact and sturdy", "A bit pricey"],
        },
        "P010": {
            "name": "Smartwatch",
            "description": "Fitness smartwatch with heart rate monitor and GPS.",
            "price": 149.99,
            "specs": {"battery": "7 days", "features": "GPS, Heart rate, Notifications"},
            "stock": 7,
            "reviews": ["Great features", "Stylish design", "App needs improvement"],
        },
        "P011": {
            "name": "Gaming Mouse Pad",
            "description": "Large, optimized surface for gaming mice.",
            "price": 19.99,
            "specs": {"size": "Large", "material": "Fabric"},
            "stock": 40,
            "reviews": ["Smooth glide", "Good value"]
        },
        "P012": {
            "name": "Ergonomic Office Chair",
            "description": "Adjustable chair with lumbar support.",
            "price": 249.99,
            "specs": {"material": "Mesh", "adjustability": "Full"},
            "stock": 3,
            "reviews": ["Very comfortable", "Easy to assemble"]
        },
        "P013": {
            "name": "Portable Projector",
            "description": "Mini projector for home cinema or presentations.",
            "price": 199.99,
            "specs": {"resolution": "720p", "connectivity": "HDMI, USB"},
            "stock": 6,
            "reviews": ["Compact", "Decent picture for size"]
        }
    },

    # --- Order Data ---
    "ORDER_DATABASE": {
        "ORD123": {
            "customer_email": "alice@example.com",
            "order_date": "2025-05-10",
            "status": "Shipped",
            "tracking_number": "TRK789XYZ",
            "carrier": "DHL",
            "expected_delivery": "2025-06-21",
            "items": [
                {"product_id": "P001", "quantity": 1},
                {"product_id": "P004", "quantity": 1}
            ],
            "total_amount": 25.99 + 39.99 # Calculates based on product prices
        },
        "ORD145": {
            "customer_email": "alice@example.com",
            "order_date": "2025-06-01",
            "status": "Processing",
            "tracking_number": None,
            "carrier": None,
            "expected_delivery": None,
            "items": [
                {"product_id": "P007", "quantity": 1},
                {"product_id": "P011", "quantity": 2}
            ],
            "total_amount": 99.99 + (19.99 * 2)
        },
        "ORD101": {
            "customer_email": "bob@example.com",
            "order_date": "2025-04-15",
            "status": "Delivered",
            "tracking_number": "TRK111ABC",
            "carrier": "UPS",
            "expected_delivery": "2025-04-20",
            "items": [
                {"product_id": "P002", "quantity": 1},
                {"product_id": "P003", "quantity": 1},
                {"product_id": "P005", "quantity": 1}
            ],
            "total_amount": 59.99 + 179.99 + 29.99
        },
        "ORD102": {
            "customer_email": "bob@example.com",
            "order_date": "2025-06-10",
            "status": "Shipped",
            "tracking_number": "TRK222DEF",
            "carrier": "FedEx",
            "expected_delivery": "2025-06-25",
            "items": [
                {"product_id": "P006", "quantity": 2},
                {"product_id": "P009", "quantity": 1}
            ],
            "total_amount": (49.99 * 2) + 129.99
        },
        "ORD200": {
            "customer_email": "charlie@example.com",
            "order_date": "2025-06-15",
            "status": "Pending",
            "tracking_number": None,
            "carrier": None,
            "expected_delivery": None,
            "items": [
                {"product_id": "P012", "quantity": 1},
                {"product_id": "P013", "quantity": 1},
                {"product_id": "P008", "quantity": 1}
            ],
            "total_amount": 249.99 + 199.99 + 89.99
        }
    },

    # --- CRM Data (User Data) ---
    "CRM_DATABASE": {
        "alice@example.com": {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "phone": "+1-555-1234",
            "address": "123 Main St, Springfield",
            "membership_level": "Gold",
            "preferences": ["tech accessories", "noise-cancelling"],
            "account_status": "Active",
            "last_contact": "2025-06-01",
            "support_tickets": [
                {"ticket_id": "TCK001", "issue": "Wrong item delivered", "status": "Resolved"},
            ],
            "orders": ["ORD123", "ORD145"] # Linked to ORDER_DATABASE
        },
        "bob@example.com": {
            "name": "Bob Smith",
            "email": "bob@example.com",
            "phone": "+1-555-5678",
            "address": "456 Elm St, Metropolis",
            "membership_level": "Silver",
            "preferences": ["gaming gear", "monitors"],
            "account_status": "Active",
            "last_contact": "2025-06-10",
            "support_tickets": [
                {"ticket_id": "TCK002", "issue": "Late delivery for ORD101", "status": "Closed"},
            ],
            "orders": ["ORD101", "ORD102"] # Linked to ORDER_DATABASE
        },
        "charlie@example.com": {
            "name": "Charlie Brown",
            "email": "charlie@example.com",
            "phone": "+1-555-9012",
            "address": "789 Pine Ave, Peanuts Town",
            "membership_level": "Bronze",
            "preferences": ["office equipment", "portable devices"],
            "account_status": "Active",
            "last_contact": "2025-06-15",
            "support_tickets": [],
            "orders": ["ORD200"] # Linked to ORDER_DATABASE
        }
    }
}

# --- Helper function for calculating total amount dynamically (optional but good practice) ---
# This function would be used *outside* the COMBINED_DATA dictionary
# if you want to calculate totals at runtime or populate them initially.
def calculate_order_total(order_id: str) -> float:
    """Calculates the total amount for an order based on product prices."""
    order = COMBINED_DATA["ORDER_DATABASE"].get(order_id)
    if not order:
        return 0.0

    total = 0.0
    for item in order.get("items", []):
        product_id = item.get("product_id")
        quantity = item.get("quantity", 0)
        product = COMBINED_DATA["PRODUCT_CATALOG"].get(product_id)
        if product:
            total += product.get("price", 0.0) * quantity
    return total

# Example of how to access data:
# all_products = COMBINED_DATA["PRODUCT_CATALOG"]
# all_orders = COMBINED_DATA["ORDER_DATABASE"]
# all_customers = COMBINED_DATA["CRM_DATABASE"]

# Accessing Alice's details:
# alice_info = COMBINED_DATA["CRM_DATABASE"]["alice@example.com"]
# print("Alice's Info:", alice_info)

# Accessing one of Alice's orders:
# alice_first_order_id = COMBINED_DATA["CRM_DATABASE"]["alice@example.com"]["orders"][0]
# alice_first_order_details = COMBINED_DATA["ORDER_DATABASE"][alice_first_order_id]
# print("\nAlice's First Order Details:", alice_first_order_details)

# Accessing a product from an order:
# first_item_in_alice_first_order_id = alice_first_order_details["items"][0]["product_id"]
# first_item_details = COMBINED_DATA["PRODUCT_CATALOG"][first_item_in_alice_first_order_id]
# print("\nDetails of first item in Alice's first order:", first_item_details)