def products_schema(parent: dict):
    return {
        "parent": parent,
        "icon": {"type": "emoji", "emoji": "📋"},
        "cover": {
            "type": "external",
            "external": {
                "url": "https://cdn11.bigcommerce.com/s-ljboqq8dd6/product_images/uploaded_images/bhs-track-your-order-banner.jpg"
            },
        },
        "title": [
            {"type": "text", "text": {"content": "Product Listings", "link": None}}
        ],
        "properties": {
            "Product Info": {"title": {}},
            "categories": {"multi_select": {"options": []}},
            "coupon codes (optional)": {"multi_select": {"options": []}},
            "display on site": {"checkbox": {}},
            "update": {"checkbox": {}},
            "images (must embed)": {"files": {}},
            "updated": {"last_edited_time": {}},
            "price": {"number": {"format": "dollar"}},
            "url (auto generated)": {"url": {}},
        },
    }
