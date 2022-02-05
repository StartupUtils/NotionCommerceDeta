import stripe
from dataclasses import dataclass
from CommerceApi.config import Config


@dataclass
class StripeInfo:
    product: stripe.Product
    price: stripe.Price

class StripeManager:
    def __init__(self, api_key):
        self.stripe = stripe
        self.stripe.api_key = api_key
        
    def create_product(self, title: str, images: list = []) -> stripe.Price:
        if len(images) > 8:
            images = images[:8]
        return self.stripe.Product.create(
            name=title,
            images=images,
            shippable=True,
            tax_code="txcd_99999999",
            active=True
        )
    
    def get_product(self, product_id: str): 
        return self.stripe.Product.retrieve(product_id)
    
    def get_price(self, price_id: str):
        return self.stripe.Price.retrieve(price_id)
    
    def delete(self, product_id: str):
        return self.stripe.Product.delete(product_id)
    
    def update_product(self, product_id: str, title: str, images: list):
        return self.stripe.Product.modify(product_id, name=title, images=images)
    
    def create_price(self, price: int, product_id: str):
        return self.stripe.Price.create(
          unit_amount=price,
          currency="usd",
          product= product_id,
        )
    
    def create_new_product(self, title: str, images: list, price: float):
        product = self.create_product(title, images)
        print(product.id)
        price = self.create_price(self._price(price), product.id)
        return StripeInfo(product, price)
    
    def update_listing(self, product_id, price_id, title, images, price: float):
        if len(images) > 8:
            images = images[:8]
        product_obj = self.update_product(product_id, title, images)
        price = self._price(price)
        price_obj = self.get_price(price_id)
        if price_obj.unit_amount != price:
            price_obj = self.create_price(price, product_id)
        return StripeInfo(product_obj, price_obj)
        
    def _price(self, price: float):
        return int(price * 100)

    def create_link(self, listings):
        YOUR_DOMAIN = "https://matthewlsession.com"
        checkout_session = stripe.checkout.Session.create(
            shipping_address_collection={
            'allowed_countries': ['US'],
            },
            line_items=listings,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        return checkout_session
        