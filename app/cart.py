from collections import Counter
from fastapi import APIRouter, HTTPException
from app.supermarket import items_db
from app.utils import validate_item_code

cart_router = APIRouter()
cart = {}

@cart_router.get("/")
def get_cart_items():
   	return cart

@cart_router.post("/reset")
def reset_cart():
	cart.clear()
	return {"message": "Cart has been reset."}

@cart_router.post("/add")
def add_to_cart(items: str):
    items = items.upper()
    item_counts = Counter(items)

    for item_name in item_counts:
        if not validate_item_code(item_name) or item_name not in items_db:
            raise HTTPException(status_code=400, detail="Bad input. One or more items are invalid.")

    for item_name, quantity in item_counts.items():
        cart[item_name] = cart.get(item_name, 0) + quantity

    return {"message": f"Items added to cart.", "cart": cart}

@cart_router.post("/remove")
def remove_from_cart(items: str):
    items = items.upper()
    item_counts = Counter(items)

    for item_name in item_counts:
        if not validate_item_code(item_name) or item_name not in cart:
            raise HTTPException(status_code=400, detail="Bad input. One or more items are not in the cart.")
        if cart[item_name] < item_counts[item_name]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot remove more than {cart[item_name]} of {item_name}."
            )

    for item_name, quantity in item_counts.items():
        cart[item_name] -= quantity
        if cart[item_name] == 0:
            del cart[item_name]

    return {"message": f"Items removed from cart.", "cart": cart}

@cart_router.get("/total-price")
def calculate_total_price():
    total = 0
    for item_name, quantity in cart.items():
        item = items_db[item_name]
        unit_price = item["unit_price"]
        special_price = item.get("special_price")

        if special_price:
            special_qty = special_price["quantity"]
            special_price_value = special_price["price"]

            total += (quantity // special_qty) * special_price_value
            total += (quantity % special_qty) * unit_price
        else:
            total += quantity * unit_price
    return {"total_price": total}
