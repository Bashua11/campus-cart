
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
    def __init__(
        self, item_id, name, price, stock=999999, validity_days=30
    ):
        super().__init__(item_id, name, price, stock)
        self.validity_days = int(validity_days)

    def __str__(self):
        return "{} - Digital Voucher (${:.2f})".format(
            self.name, self.price
        )
