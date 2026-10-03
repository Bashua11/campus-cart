def display_catalog(inventory):
	print("\n+----------------------------------------------+")
	print("  |	CAMPUS CART CATALOG			|")
	print("  +----------------------------------------------+")
	for items_id, item in inventory.items():
		print(
			f"ID: {items_id} | "
			f"Name: {item['name']} |"
			f"Price: ${item['price']:.2f} |"
			f"Stock: {item['stock']}"
		)
	print("================================================")


def verify_stock(inventory,items_id,requested_qty):
	if items_id not in inventory:
		return False
	if requested_qty <= 0:
		return False
	return requested_qty <= inventory[items_id]["stock"]

def update_stock(inventory, items_id, quantity):
	if items_id not in inventory:
		return False
	stock_update = inventory[items_id]["stock"] + quantity
	if stock_update < 0:
		return False
	inventory[items_id]["stock"] = stock_update
	return True

def calc_price(item,quantity):
	return item["price"] * quantity

def filter_available_products(inventory):
	available_products = filter(
		lambda item: item["stock"] > 0,
		inventory.values()
	)
	return list(available_products)

def sort_product_by_price(inventory):
	return sorted(
		inventory.values(),
		key=lambda item: item["price"]
	)

inventory = {
	"101": {"name": "Notebook", "price": 24.50, "stock": 21},
	"102": {"name": "Pen", "price": 12.10, "stock": 29}
} 
