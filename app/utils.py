import re

def validate_item_code(item_code: str) -> bool:
    if re.match(r'^[A-Z]$', item_code):
        return True
    return False
