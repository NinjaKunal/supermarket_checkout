import re

def validate_item_code(item_code: str) -> bool:
    """Validate that the item code is a valid single alphabet letter."""
    if re.match(r'^[A-Z]$', item_code):
        return True
    return False
