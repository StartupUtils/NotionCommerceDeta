from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4, UUID


class CartItem(BaseModel):
    id: str
    quant: int
    message: str = None


class Product(BaseModel):
    key: str
    categories: list = []
    coupons: list = []
    display: bool
    images: list = []
    more_info_section: list = []
    price: float = None
    title: str = None
    price_id: str = None

    @property
    def image(self):
        if len(self.images) > 0:
            return self.images[0]

    def total_price(self, quant: int):
        return round(self.price * quant, 2)

    def prep(self, item: CartItem):
        return {
            "price": self.price,
            "image": self.image,
            "quant": item.quant,
            "id": item.id,
            "message": item.message,
            "title": self.title,
        }


class Cart(BaseModel):
    data: List[CartItem]


def create_uuid():
    return str(uuid4())


class CuratedCart(BaseModel):
    data: List[CartItem] = Field(default_factory=list)
    key: str = Field(default_factory=create_uuid)
    message: str = None
    email: str = None

    def updatecart(self, item: CartItem):
        for i, item_in_cart in enumerate(self.data):
            if item_in_cart.id == item.id:
                self.data[i] = item
                return
        self.data.append(item)

    def removeitem(self, item_id: str):
        for i, item in enumerate(self.data):
            if item.id == item_id:
                self.data.pop(i)
                return

    def add(self, item_id: str):
        for item in self.data:
            if item.id == item_id:
                item.quant += 1

    def neg(self, item_id: str):
        for item in self.data:
            if item.id == item_id:
                if item.quant > 1:
                    item.quant -= 1


class ModCommand(BaseModel):
    command: str
    order_key: str
    product_key: str
