
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
