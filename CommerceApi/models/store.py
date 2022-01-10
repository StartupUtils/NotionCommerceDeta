from pydantic import BaseModel, Field


class Product(BaseModel):
    key: str
    categories: list = []
    coupons: list = []
    display: bool
    images: list = []
    more_info_section: list = []
    price: float = None
    
