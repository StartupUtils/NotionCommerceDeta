from CommerceApi.config import Config

order_content_block = {
    "children": [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "text": [
                    {
                        "type": "text",
                        "text": {"content": "Manage Orders"},
                        "annotations": {"underline": True},
                    }
                ]
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Managing products entails being able to add new products, edit details of existing products, modify the price of any given product, upload and change product photos, and manage promotions/discounts."
                        },
                    }
                ]
            },
        },
    ]
}

product_content_block = {
    "children": [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "text": [
                    {
                        "type": "text",
                        "text": {"content": "Manage Products"},
                        "annotations": {"underline": True},
                    }
                ]
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Managing products entails being able to add new products, edit details of existing products, modify the price of any given product, upload and change product photos, and manage promotions/discounts."
                        },
                    }
                ]
            },
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "text": [
                    {
                        "type": "text",
                        "text": {"content": "👇 Manage Product Listings"},
                    }
                ]
            },
        },
    ]
}

example_product_page = {
    "children": [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "text": [
                    {
                        "type": "text",
                        "text": {
                            "content": """This is placeholder content for a product page. The divider after the bullet points separates the “feature section” and the “more info section”. The section before the divider is the feature section and will be located next to the product pictures. The section after the divider will be positioned below the product pictures. Product content can include all headings, paragraphs, bullet points, and images (embedded only). Delete all this content and fill it in with your own."""
                        },
                    }
                ]
            },
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "text": [
                    {
                        "type": "text",
                        "text": {"content": "Feature example one."},
                    }
                ]
            },
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "text": [
                    {
                        "type": "text",
                        "text": {"content": "Feature example two."},
                    }
                ]
            },
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "text": [
                    {
                        "type": "text",
                        "text": {"content": "Feature example three."},
                    }
                ]
            },
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {},
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "text": [
                    {
                        "type": "text",
                        "text": {"content": "Example heading for More Info Section"},
                    }
                ]
            },
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Example dummy text for a paragraph in the More Info Section with an embedded image."
                        },
                    }
                ]
            },
        },
        {
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {
                    "url": "https://image.shutterstock.com/image-vector/set-different-beauty-cosmetic-products-260nw-1942263496.jpg"
                },
            },
        },
    ]
}


def image_manager_content_block(uuid):
    return {
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "text": [
                        {
                            "type": "text",
                            "text": {"content": "Upload & Manage Product Images"},
                            "annotations": {"underline": True},
                        }
                    ]
                },
            },
            {
                "object": "block",
                "type": "embed",
                "embed": {"url": f"{Config.base_url}/manage_image/load/{uuid}"},
            },
            {
                "object": "block",
                "type": "embed",
                "embed": {"url": f"{Config.base_url}/manage_image/show/{uuid}"},
            },
        ]
    }
