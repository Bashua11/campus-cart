"""
CampusCart - a CLI tool for campus vendors to track stock,
add up customer totals, and print receipts.
"""
# Author: Luqman.

# The vendor chooses their preferred action on the CLI
# choice = input("Choose an option: ").strip().lower()

# The vendor chooses quantity of item when adding item to cart
# quantity = int(input("How many? "))

inventory = {
    "201": {"name": "Blue Oud", "price": 50.00, "stock": 8},
    "202": {"name": "9 PM Rebel", "price": 70.00, "stock": 3},
    "203": {"name": "club de nuit.", "price": 100.00, "stock": 5}
}
cart = []
while True:
    print("1. View catalog")
    print("2. Add to cart")
    print("3. View cart")
    print("4. Checkout")
    print("5. Exit")

    choice = input("Choose an option: ").strip().lower()

    if choice == "1":
        print("--- Catalog ---")
        for item_id in inventory:
            name = inventory[item_id]["name"]
            price = inventory[item_id]["price"]
            stock = inventory[item_id]["stock"]
            print(f"{item_id}: {name}, ${price:.2f}, stock: {stock}")  
    elif choice == "2":
        input_item_id = input("Enter the item ID to add to cart: ").strip()
        if input_item_id in inventory:
            available_stock = inventory[input_item_id]["stock"]
            quantity = int(input(f"How many of {inventory[input_item_id]['name']} would you like to add? (Available stock: {available_stock}): "))
            if quantity <= available_stock:
                 subtotal = inventory[input_item_id]["price"] * quantity
                 cart.append({"id": input_item_id, "qty": quantity, "subtotal": subtotal})
                 print(f"Added {quantity} x {inventory[input_item_id]['name']} to cart. Subtotal: ${subtotal:.2f}")
            else:
                 print("Not enough stock. Only", available_stock, "available.")
        else:
            print("Item not found in inventory.")
    elif choice == "3":
        if not cart:
            print("Your cart is empty.")
        else:
            print("--- Cart ---")
            total = 0
            for item in cart:
                item_id = item["id"]
                quantity = item["qty"]
                subtotal = item["subtotal"]
                name = inventory[item_id]["name"]
                price = inventory[item_id]["price"]
                print(f"{name}: {quantity} x ${price:.2f} = ${subtotal:.2f}")
                total = total + subtotal
            print(f"Total: ${total:.2f}")
    elif choice == "4":
        if not cart:
            print("Your cart is empty. Nothing to check out.")
        else:
            print("\n--- Receipt ---")
            total = 0
            for item in cart:
                item_id = item["id"]
                quantity = item["qty"]
                subtotal = item["subtotal"]
                name = inventory[item_id]["name"]
                print(f"{name}: {quantity} x ${inventory[item_id]['price']:.2f} = ${subtotal:.2f}")
                total = total + subtotal

            discount = 0
            if total > 20:
                discount = total * 0.10
                total = total - discount
                print(f"Discount (10%): -${discount:.2f}")

            print(f"Total amount due: ${total:.2f}")
            print("---------------\n")

            for item in cart:
                inventory[item["id"]]["stock"] -= item["qty"]

            cart.clear()
            print("Checkout complete. Thank you!")
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, please pick 1-5")


