def orders_schema(parent: dict):
    return {
        "parent": parent,
        "icon": {"type": "emoji", "emoji": "📦"},
        "cover": {
            "type": "external",
            "external": {
                "url": "https://thumbs.dreamstime.com/b/shopping-cart-blue-background-minimalism-style-creative-design-top-view-copy-space-shop-trolley-shopping-cart-blue-121788283.jpg"
            },
        },
        "title": [{"type": "text", "text": {"content": "orders", "link": None}}],
        "properties": {
            "order details": {"title": {}},
            "status": {
                "select": {
                    "options": [
                        {"name": "new", "color": "blue"},
                        {"name": "completed", "color": "green"},
                        {"name": "refunded", "color": "yellow"},
                        {"name": "shipped", "color": "orange"},
                    ]
                }
            },
            "order id": {"rich_text": {}},
            "address": {"rich_text": {}},
            "email": {"email": {}},
            "phone": {"phone_number": {}},
            "order date": {"created_time": {}},
            "order price": {"number": {"format": "dollar"}},
            "receipt": {"url": {}},
        },
    }


def add_order_schema(
    parent_id,
    title,
    order_id,
    address,
    price,
    email,
    receipt,
):
    return {
        "parent": {"type": "database_id", "database_id": parent_id},
        "properties": {
            "order details": {
                "title": [{"type": "text", "text": {"content": title, "link": None}}]
            },
            "email": {"email": email},
            "status": {"select": {"name": "new"}},
            "order id": {"rich_text": [{"text": {"content": order_id}}]},
            "address": {"rich_text": [{"text": {"content": address}}]},
            "receipt": {"url": receipt},
            "order price": {"number": price},
        },
    }


def _create_order_check(title: str, sku: str, link: str):
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "text": [
                {
                    "type": "text",
                    "text": {"content": f"{title} - ", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "title of product - ",
                    "href": None,
                },
                {
                    "type": "text",
                    "text": {"content": sku, "link": {"url": link}},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "88382",
                    "href": "https://matthewlsessions.com",
                },
            ],
            "checked": False,
        },
    }
