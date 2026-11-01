
from decimal import Decimal


class ShoppingCart:
    def __init__(self):
        self._items = {}

    @property
    def items(self):
        return [
            {
                "item": details["item"],
                "quantity": details["quantity"],
                "subtotal": (
                    details["item"].price * details["quantity"]
                ).quantize(Decimal("0.01"))
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
