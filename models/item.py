cat > models/item.py <<'PY'
from datetime import date
from decimal import Decimal


def money(value):
    return Decimal(str(value)).quantize(Decimal("0.01"))


class Item:
    def __init__(self, item_id, name, price, stock):
        self._item_id = str(item_id)
        self._name = name
        self._price = money(price)
        self._stock = int(stock)

        if self._price < 0 or self._stock < 0:
            raise ValueError("Price and stock cannot be negative.")

    @property
    def item_id(self):
        return self._item_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock

    def update_stock(self, quantity):
        new_stock = self._stock + int(quantity)
        if new_stock < 0:
            raise ValueError("Insufficient stock.")
        self._stock = new_stock
        return self._stock

    def __str__(self):
        return "{} - ${:.2f} ({} available)".format(
            self.name, self.price, self.stock
        )


class PerishableItem(Item):
    def __init__(self, item_id, name, price, stock, expiry_date):
        super().__init__(item_id, name, price, stock)
        if isinstance(expiry_date, str):
            expiry_date = date.fromisoformat(expiry_date)
        self.expiry_date = expiry_date

    def is_expired(self):
        return self.expiry_date < date.today()


class DigitalVoucher(Item):
    def __init__(self, item_id, name, price, stock=999999, validity_days=30):
        super().__init__(item_id, name, price, stock)
        self.validity_days = int(validity_days)

    def __str__(self):
        return "{} - Digital Voucher (${:.2f})".format(
            self.name, self.price
        )
PY

cat > models/cart.py <<'PY'
from decimal import Decimal
from .item import money


class ShoppingCart:
    def __init__(self):
        self._items = {}

    @property
    def items(self):
        return [
            {
                "item": details["item"],
                "quantity": details["quantity"],
                "subtotal": money(
                    details["item"].price * details["quantity"]
                )
            }
            for details in self._items.values()
        ]

    def add_item(self, item, quantity):
        quantity = int(quantity)

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        current_quantity = self._items.get(
            item.item_id, {}
        ).get("quantity", 0)

        if current_quantity + quantity > item.stock:
            raise ValueError("Requested quantity exceeds available stock.")

        if item.item_id in self._items:
            self._items[item.item_id]["quantity"] += quantity
        else:
            self._items[item.item_id] = {
                "item": item,
                "quantity": quantity
            }

    def remove_item(self, item_id):
        if str(item_id) in self._items:
            del self._items[str(item_id)]

    def update_quantity(self, item_id, quantity):
        item_id = str(item_id)
        quantity = int(quantity)

        if item_id not in self._items:
            raise KeyError("Item is not in the cart.")

        if quantity <= 0:
            self.remove_item(item_id)
            return

        item = self._items[item_id]["item"]
        if quantity > item.stock:
            raise ValueError("Requested quantity exceeds available stock.")

        self._items[item_id]["quantity"] = quantity

    def calculate_subtotal(self):
        return sum(
            (
                details["item"].price * details["quantity"]
                for details in self._items.values()
            ),
            Decimal("0.00")
        )

    def clear(self):
        self._items.clear()

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return sum(
            details["quantity"] for details in self._items.values()
        )
PY

cat > models/payment.py <<'PY'
from abc import ABC, abstractmethod
from uuid import uuid4


class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class CashPayment(Payment):
    def process_payment(self, amount):
        return {
            "success": True,
            "method": "Cash",
            "amount": str(amount),
            "transaction_id": str(uuid4())[:8].upper(),
            "message": "Cash payment recorded successfully."
        }


class CardPayment(Payment):
    def process_payment(self, amount):
        return {
            "success": True,
            "method": "Card",
            "amount": str(amount),
            "transaction_id": str(uuid4())[:8].upper(),
            "message": "Demo card payment approved."
        }


class MobileMoneyPayment(Payment):
    def process_payment(self, amount):
        return {
            "success": True,
            "method": "Mobile Money",
            "amount": str(amount),
            "transaction_id": str(uuid4())[:8].upper(),
            "message": "Demo mobile money payment approved."
        }
PY

cat > models/__init__.py <<'PY'
from .item import Item, PerishableItem, DigitalVoucher
from .cart import ShoppingCart
from .payment import Payment, CashPayment, CardPayment, MobileMoneyPayment

__all__ = [
    "Item",
    "PerishableItem",
    "DigitalVoucher",
    "ShoppingCart",
    "Payment",
    "CashPayment",
    "CardPayment",
    "MobileMoneyPayment"
]
PY