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
        print("Add to cart")

    elif choice == "3":
        print("View cart")

    elif choice == "4":
        print("Checkout")

    elif choice == "5":
        print("Thank you for using CampusCart!")
        break

    else:
        print("Invalid choice. Please select 1-5.")