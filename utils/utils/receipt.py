
def stream_receipt_lines(cart, delivery_fee=0, discount=0, total=None):
    if cart.is_empty():
        yield "Your cart is empty."
        return

    yield "========== CAMPUSCART RECEIPT =========="

    for line in cart.items:
        item = line["item"]
        quantity = line["quantity"]
        subtotal = line["subtotal"]

        yield "{} | {} x ${:.2f} = ${:.2f}".format(
            item.name, quantity, item.price, subtotal
        )

    yield "-----------------------------------------"
    yield "Subtotal: ${:.2f}".format(cart.calculate_subtotal())
    yield "Discount: -${:.2f}".format(discount)
    yield "Delivery fee: ${:.2f}".format(delivery_fee)

    if total is not None:
        yield "TOTAL: ${:.2f}".format(total)

    yield "========================================="
    yield "Thank you for shopping with CampusCart!"
