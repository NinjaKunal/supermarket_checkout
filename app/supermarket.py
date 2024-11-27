from fastapi import APIRouter, HTTPException
from app.models import Item
from app.utils import validate_item_code

supermarket_router = APIRouter()

items_db = {}

@supermarket_router.get("/")
def fetch_all_items():
    return items_db

@supermarket_router.post("/")
def add_item(item: Item):
    if not validate_item_code(item.item_name):
      raise HTTPException(status_code=400, detail="Invalid item code. Use a single uppercase letter.")
    if item.item_name in items_db:
      raise HTTPException(status_code=400, detail="Item already exists.")
    items_db[item.item_name] = item.dict()
    return item

@supermarket_router.delete("/{item_name}")
def delete_item(item_name: str):
    if not validate_item_code(item_name):
      raise HTTPException(status_code=400, detail="Invalid item code. Use a single uppercase letter.")
    if item_name not in items_db:
      raise HTTPException(status_code=404, detail="Item not found.")
    del items_db[item_name]
    return {"message": f"Item {item_name} deleted."}

@supermarket_router.get("/{item_name}/price-rule")
def get_price_rule(item_name: str):
    if not validate_item_code(item_name):
      raise HTTPException(status_code=400, detail="Invalid item code. Use a single uppercase letter.")
    return items_db.get(item_name, {"error": "Item not found."})
