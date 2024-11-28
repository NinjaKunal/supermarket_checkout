from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    item_name: str
    unit_price: int
    special_price: Optional[dict] = None
