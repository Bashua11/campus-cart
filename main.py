"""
CampusCart - Stage 2
A command-line shopping cart application.

Author: Elizabeth Bashua
"""

# Product inventory
inventory = {
    "101": {"name": "Notebook", "price": 2.50, "stock": 15},
    "102": {"name": "Pen", "price": 1.50, "stock": 20},
    "103": {"name": "Backpack", "price": 18.00, "stock": 8},
    "104": {"name": "Calculator", "price": 12.00, "stock": 10},
    "105": {"name": "Water Bottle", "price": 7.50, "stock": 12}
}

# Empty shopping cart
cart = []

while True:
    print("\n===== CAMPUSCART =====")
    print("1. View Catalog")
    print("2. Add Item to Cart")
    print("3. View Cart")
    print("4. Checkout")
    print("5. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        print("\n===== PRODUCT CATALOG =====")

        for product_id, product in inventory.items():
            print(
                f"{product_id} | "
                f"{product['name']} | "
                f"${product['price']:.2f} | "
                f"Stock: {product['stock']}"
            )
            
        elif choice == "2":
        product_id = input("Enter the product ID: ").strip()

        if product_id not in inventory:
            print("Invalid product ID.")
            continue

        try:
            quantity = int(input("Enter quantity: "))

            if quantity <= 0:
                print("Quantity must be greater than zero.")
                continue

            product = inventory[product_id]

            quantity_in_cart = 0

for item in cart:
    if item["id"] == product_id:
        quantity_in_cart += item["qty"]

available_stock = product["stock"] - quantity_in_cart

if quantity > available_stock:
    print(
        f"Insufficient stock. "
        f"Only {available_stock} available."
    )
    continue

            subtotal = product["price"] * quantity

            cart.append({
                "id": product_id,
                "name": product["name"],
                "price": product["price"],
                "qty": quantity,
                "subtotal": subtotal
            })

            print(f"{quantity} x {product['name']} added to cart.")

        except ValueError:
            print("Invalid quantity. Please enter a number.")

        elif choice == "3":
        if not cart:
            print("Your cart is empty.")
        else:
            print("\n===== YOUR CART =====")
            cart_total = 0

            for item in cart:
                print(
                    f"{item['name']} | "
                    f"Qty: {item['qty']} | "
                    f"${item['subtotal']:.2f}"
                )
                cart_total += item["subtotal"]

            print(f"Cart Total: ${cart_total:.2f}")

        elif choice == "4":
        if not cart:
            print("Your cart is empty. Add items before checkout.")
            continue

        subtotal = 0

        for item in cart:
            subtotal += item["subtotal"]

        # Apply a 10% discount to orders over $20
        if subtotal > 20:
            discount = subtotal * 0.10
        else:
            discount = 0

        total = subtotal - discount

        print("\n===== CAMPUSCART RECEIPT =====")

        for item in cart:
            print(
                f"{item['name']} | "
                f"Qty: {item['qty']} | "
                f"${item['subtotal']:.2f}"
            )

        print("------------------------------")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Discount: ${discount:.2f}")
        print(f"Total: ${total:.2f}")
        print("------------------------------")
        print("Thank you for shopping with CampusCart!")

        # Deduct purchased quantities from inventory
        for item in cart:
            inventory[item["id"]]["stock"] -= item["qty"]

        # Empty the cart after successful checkout
        cart.clear()

    elif choice == "5":
        print("Thank you for using CampusCart!")
        break

    else:
        print("Invalid choice. Please select 1-5.")