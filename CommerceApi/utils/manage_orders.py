from dataclasses import dataclass
from CommerceApi.Notion import orders


@dataclass
class Address:
    city: str
    line1: str
    line2: str
    postal_code: str
    state: str
    country: str

    @property
    def address_str(self):
        street = f"{self.line1} {self.line2}" if self.line2 else self.line1
        return f"{street} {self.city}, {self.state}, {self.postal_code}"


class ManageOrder:
    def __init__(self, order: dict):
        self._address = order.get("address")
        self._amount = order.get("amount")
        self.name = order.get("name")
        self.key = order.get("key")
        self.email = order.get("email")
        self.receipt = order.get("receipt")

    @property
    def address(self) -> str:
        address = Address(**self._address)
        return address.address_str

    @property
    def amount(self):
        if self._amount:
            return self._amount / 100

    @property
    def title(self):
        return f"Order from {self.name}"

    def prep(self, parent_id: str) -> dict:
        return orders.add_order_schema(
            parent_id,
            self.title,
            self.key,
            self.address,
            self.amount,
            self.email,
            self.receipt,
        )
