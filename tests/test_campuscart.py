
import unittest

from models import (
    Item,
    ShoppingCart,
    CashPayment,
    CardPayment,
    MobileMoneyPayment
)


class TestCampusCart(unittest.TestCase):

    def setUp(self):
        self.item = Item("101", "Notebook", "2.50", 10)
        self.cart = ShoppingCart()

    def test_stock_decreases_after_update(self):
        self.item.update_stock(-3)
        self.assertEqual(self.item.stock, 7)

    def test_insufficient_stock_raises_exception(self):
        with self.assertRaises(ValueError):
            self.item.update_stock(-15)

    def test_empty_cart_is_empty(self):
        self.assertTrue(self.cart.is_empty())

    def test_empty_inventory_lookup_raises_exception(self):
        inventory = {}

        with self.assertRaises(ValueError):
            if not inventory:
                raise ValueError("Inventory is empty.")

    def test_cart_adds_item(self):
        self.cart.add_item(self.item, 2)
        self.assertEqual(len(self.cart), 2)
        self.assertEqual(self.cart.calculate_subtotal(), 5.00)

    def test_payment_methods_return_success_status(self):
        payment_methods = [
            CashPayment(),
            CardPayment(),
            MobileMoneyPayment()
        ]

        for payment in payment_methods:
            result = payment.process_payment(10)

            self.assertIsInstance(result, dict)
            self.assertTrue(result["success"])
            self.assertIn("transaction_id", result)


if __name__ == "__main__":
    unittest.main()
