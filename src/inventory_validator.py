def is_valid_sku(sku):
    """Return True for SKUs like INV-1234."""
    if not isinstance(sku, str):
        raise TypeError("sku must be a string")
    parts = sku.split("-")
    return len(parts) == 2 and parts[0] == "INV" and parts[1].isdigit() and len(parts[1]) == 4


def normalize_sku(sku):
    """Return a normalized SKU."""
    if not is_valid_sku(sku):
        raise ValueError("invalid sku")
    return sku.upper()


def stock_status(quantity, reorder_level):
    """Return stock status based on quantity."""
    if quantity < 0 or reorder_level < 0:
        raise ValueError("quantities cannot be negative")
    if quantity == 0:
        return "OUT_OF_STOCK"
    if quantity <= reorder_level:
        return "REORDER"
    return "OK"


def format_item(name, sku, quantity):
    """Return a display string for an inventory item."""
    if not name.strip():
        raise ValueError("name required")
    if not is_valid_sku(sku):
        raise ValueError("invalid sku")
    if quantity < 0:
        raise ValueError("quantity cannot be negative")
    return f"{name.strip()} [{sku}] - {quantity}"
