"""
CampusCart - a CLI tool for campus vendors to track stock,
add up customer totals, and print receipts.
"""
# Author: Luqman.

# The vendor chooses their preferred action on the CLI
choice = input("Choose an option: ").strip().lower()

# The vendor chooses quantity of item when adding item to cart
quantity = int(input("How many? "))

inventory = {
    "201": {"name": "Blue Oud", "price": 50.00, "stock": 8},
    "202": {"name": ".9 PM Rebel", "price": 70.00, "stock": 3},
    "203": {"name": "club de nuit.", "price": 100.00, "stock": 5}
}
cart = []