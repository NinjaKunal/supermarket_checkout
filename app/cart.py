from fastapi import APIRouter, HTTPException
from app.models import CartItem
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
def add_to_cart(cart_item: CartItem):
	if not validate_item_code(cart_item.item_name):
		raise HTTPException(status_code=400, detail="Invalid item code. Use a single uppercase letter.")
	if cart_item.item_name not in items_db:
		raise HTTPException(status_code=404, detail="Item not found in the store.")
	cart[cart_item.item_name] = cart.get(cart_item.item_name, 0) + cart_item.quantity
	return {"message": f"{cart_item.quantity} of {cart_item.item_name} added to cart."}


@cart_router.post("/remove")
def remove_from_cart(cart_item: CartItem):
	if not validate_item_code(cart_item.item_name):
		raise HTTPException(status_code=400, detail="Invalid item code. Use a single uppercase letter.")
	if cart_item.item_name not in cart:
		raise HTTPException(status_code=404, detail="Item not in the cart.")
	if cart[cart_item.item_name] < cart_item.quantity:
		raise HTTPException(status_code=400, detail=f"Cannot remove more than {cart[cart_item.item_name]} of {cart_item.item_name}.")
	cart[cart_item.item_name] -= cart_item.quantity
	if cart[cart_item.item_name] == 0:
		del cart[cart_item.item_name]
	return {"message": f"{cart_item.quantity} of {cart_item.item_name} removed from cart."}

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
