
import streamlit as st
from decimal import Decimal

from models import (
    Item,
    PerishableItem,
    DigitalVoucher,
    ShoppingCart,
    CashPayment,
    CardPayment,
    MobileMoneyPayment
)
from utils import (
    log_transaction,
    transaction_logs,
    get_audit_summary,
    stream_receipt_lines
)


DELIVERY_FEE = Decimal("2.00")
FREE_DELIVERY_LIMIT = Decimal("30.00")
COUPON_CODE = "CAMPUS10"


def create_inventory():
    return {
        "101": Item("101", "Notebook", "2.50", 20),
        "102": Item("102", "Pen", "1.50", 15),
        "103": Item("103", "Water Bottle", "5.00", 12),
        "104": Item("104", "Shirt", "8.00", 25),
        "105": PerishableItem(
            "105", "Fresh Milk", "3.50", 10, "2027-12-31"
        ),
        "106": DigitalVoucher(
            "106", "Campus Digital Voucher", "10.00", 50, 30
        )
    }


@log_transaction
def complete_checkout(cart, inventory, payment_processor, coupon):
    if cart.is_empty():
        return {"success": False, "message": "Your cart is empty."}

    subtotal = cart.calculate_subtotal()

    discount = Decimal("0.00")
    if coupon.strip().upper() == COUPON_CODE and subtotal >= Decimal("20.00"):
        discount = subtotal * Decimal("0.10")

    delivery_fee = (
        Decimal("0.00")
        if subtotal >= FREE_DELIVERY_LIMIT
        else DELIVERY_FEE
    )

    total = subtotal - discount + delivery_fee

    for line in cart.items:
        item = line["item"]
        quantity = line["quantity"]

        if quantity > item.stock:
            return {
                "success": False,
                "message": "Insufficient stock for {}.".format(item.name)
            }

        if isinstance(item, PerishableItem) and item.is_expired():
            return {
                "success": False,
                "message": "{} has expired and cannot be sold.".format(
                    item.name
                )
            }

    payment_result = payment_processor.process_payment(total)

    if not payment_result.get("success"):
        return {
            "success": False,
            "message": payment_result.get(
                "message", "Payment was unsuccessful."
            )
        }

    receipt = list(
        stream_receipt_lines(
            cart,
            delivery_fee=delivery_fee,
            discount=discount,
            total=total
        )
    )

    for line in cart.items:
        line["item"].update_stock(-line["quantity"])

    cart.clear()

    return {
        "success": True,
        "message": payment_result["message"],
        "payment": payment_result,
        "receipt": receipt,
        "total": total
    }


st.set_page_config(
    page_title="CampusCart",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 CampusCart")
st.caption("Your campus shopping experience, made simple.")

# Initialise persistent session data
if "inventory" not in st.session_state:
    st.session_state.inventory = create_inventory()

if "cart" not in st.session_state:
    st.session_state.cart = ShoppingCart()

if "last_receipt" not in st.session_state:
    st.session_state.last_receipt = None

if "last_payment" not in st.session_state:
    st.session_state.last_payment = None


inventory = st.session_state.inventory
cart = st.session_state.cart

# Dashboard metrics
total_products = len(inventory)
available_units = sum(item.stock for item in inventory.values())
cart_total = cart.calculate_subtotal()

metric1, metric2, metric3 = st.columns(3)

metric1.metric("Products", total_products)
metric2.metric("Available Units", available_units)
metric3.metric("Cart Items", len(cart))

st.divider()

st.header("Product Catalogue")
st.write("Browse the products below and add your selections to your cart.")

products = list(inventory.values())

for start in range(0, len(products), 3):
    columns = st.columns(3)

    for column, item in zip(columns, products[start:start + 3]):
        with column:
            with st.container(border=True):
                st.subheader(item.name)
                st.write("**Price:** ${:.2f}".format(item.price))
                st.write("**Stock:** {}".format(item.stock))

                if isinstance(item, PerishableItem):
                    st.caption(
                        "Perishable product | Expires: {}".format(
                            item.expiry_date
                        )
                    )
                elif isinstance(item, DigitalVoucher):
                    st.caption(
                        "Digital voucher | Valid for {} days".format(
                            item.validity_days
                        )
                    )
                else:
                    st.caption("Regular campus product")

                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=max(1, item.stock),
                    value=1,
                    step=1,
                    key="quantity_{}".format(item.item_id),
                    disabled=item.stock == 0
                )

                if st.button(
                    "Add to Cart",
                    key="add_{}".format(item.item_id),
                    use_container_width=True,
                    disabled=item.stock == 0
                ):
                    try:
                        cart.add_item(item, quantity)
                        st.toast("{} added to cart.".format(item.name))
                    except ValueError as error:
                        st.warning(str(error))

st.divider()

# Shopping cart and checkout
st.sidebar.title("🛍️ Your Shopping Cart")

if cart.is_empty():
    st.sidebar.info("Your cart is currently empty.")
else:
    for line in cart.items:
        item = line["item"]

        st.sidebar.write(
            "**{}**".format(item.name)
        )
        st.sidebar.caption(
            "{} × ${:.2f} = ${:.2f}".format(
                line["quantity"], item.price, line["subtotal"]
            )
        )

        edit_col, remove_col = st.sidebar.columns([2, 1])

        with edit_col:
            new_quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=max(1, item.stock),
                value=line["quantity"],
                key="cart_qty_{}".format(item.item_id)
            )

            if new_quantity != line["quantity"]:
                try:
                    cart.update_quantity(item.item_id, new_quantity)
                    st.rerun()
                except ValueError as error:
                    st.sidebar.warning(str(error))

        with remove_col:
            if st.button(
                "Remove",
                key="remove_{}".format(item.item_id)
            ):
                cart.remove_item(item.item_id)
                st.rerun()

        st.sidebar.divider()

subtotal = cart.calculate_subtotal()

st.sidebar.metric("Subtotal", "${:.2f}".format(subtotal))

coupon = st.sidebar.text_input(
    "Coupon code",
    placeholder="Enter CAMPUS10"
)

discount = Decimal("0.00")

if coupon.strip().upper() == COUPON_CODE:
    if subtotal >= Decimal("20.00"):
        discount = subtotal * Decimal("0.10")
        st.sidebar.success("10% discount applied!")
    else:
        st.sidebar.info("Spend at least $20 to use this coupon.")

delivery_fee = (
    Decimal("0.00")
    if cart.is_empty() or subtotal >= FREE_DELIVERY_LIMIT
    else DELIVERY_FEE
)

if delivery_fee == 0 and not cart.is_empty():
    st.sidebar.success("Free delivery applied!")
else:
    st.sidebar.info("Delivery fee: $2.00. Free delivery on orders of $30 or more.")

total = subtotal - discount + delivery_fee

st.sidebar.metric("Discount", "-${:.2f}".format(discount))
st.sidebar.metric("Delivery", "${:.2f}".format(delivery_fee))
st.sidebar.metric("Total", "${:.2f}".format(total))

st.sidebar.divider()

payment_method = st.sidebar.selectbox(
    "Select payment method",
    ["Cash", "Card", "Mobile Money"]
)

payment_processors = {
    "Cash": CashPayment,
    "Card": CardPayment,
    "Mobile Money": MobileMoneyPayment
}

if st.sidebar.button(
    "Complete Checkout",
    type="primary",
    use_container_width=True,
    disabled=cart.is_empty()
):
    processor = payment_processors[payment_method]()

    try:
        result = complete_checkout(
            cart,
            inventory,
            processor,
            coupon
        )

        if result["success"]:
            st.session_state.last_receipt = result["receipt"]
            st.session_state.last_payment = result["payment"]
            st.toast("Payment successful!")
            st.rerun()
        else:
            st.sidebar.warning(result["message"])

    except Exception as error:
        st.sidebar.error("Checkout failed: {}".format(error))

# Receipt display
if st.session_state.last_receipt:
    st.header("Latest Transaction Receipt")

    payment = st.session_state.last_payment

    st.success(payment["message"])
    st.write("**Payment method:**", payment["method"])
    st.write("**Transaction ID:**", payment["transaction_id"])

    st.code(
        "\n".join(st.session_state.last_receipt),
        language="text"
    )

    if st.button("Dismiss Receipt"):
        st.session_state.last_receipt = None
        st.session_state.last_payment = None
        st.rerun()

# Audit dashboard
st.divider()
st.header("Transaction Audit Dashboard")

audit = get_audit_summary(transaction_logs)

audit1, audit2, audit3 = st.columns(3)

audit1.metric("Total Transactions", audit["total_transactions"])
audit2.metric("Completed", audit["completed"])
audit3.metric("Failed", audit["failed"])

with st.expander("View transaction log"):
    if transaction_logs:
        st.dataframe(transaction_logs, use_container_width=True)
    else:
        st.info("No transactions have been recorded yet.")

st.caption(
    "CampusCart Stage 4 | Card and mobile-money transactions are simulated."
)
