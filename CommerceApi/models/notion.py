from pydantic import BaseModel, Field


class Parent(BaseModel):
    type: str
    database_id: str = None
    page_id: str = None

    @property
    def id(self):
        return self.page_id if self.type == "page_id" else self.database_id


class ObjectProperty(BaseModel):
    type: str


class NotionObject(BaseModel):
    object: str = None
    id: str = None
    created_time: str = None
    last_edited_time: str = None
    parent: Parent = None
    properties: dict = None


class ProductProperties(BaseModel):
    id: str
    categories_raw: dict = Field(alias="categories")
    coupons_raw: dict = Field(alias="coupon codes (optional)")
    images_raw: dict = Field(alias="images (must embed)")
    price_raw: dict = Field(alias="price")
    title_raw: dict = Field(alias="Product Info")
    display_raw: dict = Field(alias="display on site")
    selling_section: list = []
    more_info_section: list = []
    page_results: list = []
    product_id: str = None
    price_id: str = None

    @property
    def title(self):
        return self._grab_item(self.title_raw)[0].get("plain_text")

    @property
    def price(self):
        return self._grab_item(self.price_raw)

    @property
    def sku(self):
        return self._grab_item(self.sku_raw)

    @property
    def display(self):
        return self._grab_item(self.display_raw)

    @property
    def categories(self):
        return self._grab_items(self.categories_raw)

    @property
    def coupons(self):
        return self._grab_items(self.coupons_raw)

    @property
    def images(self):
        return self._grab_items(self.images_raw)

    @staticmethod
    def _grab_items(multi_select):
        key = multi_select["type"]
        return [value.get("name") for value in multi_select.get(key)]

    @staticmethod
    def _grab_item(item):
        key = item["type"]
        return item.get(key)

    def add_stripe_info(self, product_id, price_id):
        self.product_id = product_id
        self.price_id = price_id

    def prep_for_insert(self):
        return {
            "key": self.id,
            "price": self.price,
            "title": self.title,
            "display": self.display,
            "categories": self.categories,
            "coupons": self.coupons,
            "images": self.images,
            "selling_section": self.selling_section,
            "more_info_section": self.more_info_section,
            "product_id": self.product_id,
            "price_id": self.price_id,
        }


class Block(object):
    allowed_types = set(
        [
            "paragraph",
            "bulleted_list_item",
            "divider",
            "image",
            "heading_1",
            "heading_2",
            "heading_3",
            "heading_4",
            "heading_5",
        ]
    )

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def valid(self):
        return self.type in self.allowed_types

    @property
    def target(self):
        if self.type in [
            "paragraph",
            "bulleted_list_item",
            "heading_1",
            "heading_2",
            "heading_3",
            "heading_4",
            "heading_5",
        ]:
            return self.get_text()
        if self.type == "image":
            return self.get_image()

    def get_text(self):
        content = self._get_content()
        holder = content.get("text", [])
        if len(holder) > 0:
            return holder[0].get("plain_text")

    def get_image(self):
        content = self._get_content()
        return content.get("external", {}).get("url")

    def _get_content(self):
        return self.__getattribute__(self.type)


class BlockManager:
    def __init__(self, results: list):
        self.results = results
        self.selling_blocks = []
        self.more_info_blocks = []

    def populate_blocks(self):
        target = self.selling_blocks
        target_switch = 0
        for block in self.results:
            formatted_block = Block(**block)
            if formatted_block.valid:
                if formatted_block.type == "divider":
                    if target_switch == 0:
                        target = self.more_info_blocks
                    target_switch += 1
                    continue
                content = formatted_block.target
                if content:
                    target.append({formatted_block.type: content})
