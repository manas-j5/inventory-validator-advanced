import pytest

from src.inventory_validator import format_item, is_valid_sku, normalize_sku, stock_status


def test_is_valid_sku():
    assert is_valid_sku("INV-1234") is True


def test_is_valid_sku_type_error():
    with pytest.raises(TypeError):
        is_valid_sku(1234)


def test_stock_status_ok():
    assert stock_status(20, 5) == "OK"


def test_format_item():
    assert format_item(" Keyboard ", "INV-1234", 10) == "Keyboard [INV-1234] - 10"


def test_normalize_sku():
    sku = "INV-1234"
    result = normalize_sku(sku)
    assert result == "INV-1234"


def test_normalize_sku_invalid_raises_value_error():
    with pytest.raises(ValueError, match="invalid sku"):
        normalize_sku("inv-123")


def test_is_valid_sku_invalid_patterns():
    assert is_valid_sku("INV-123") is False
    assert is_valid_sku("inv-1234") is False
    assert is_valid_sku("INV-12A4") is False


def test_stock_status_out_of_stock():
    assert stock_status(0, 5) == "OUT_OF_STOCK"


def test_stock_status_reorder_at_threshold():
    assert stock_status(5, 5) == "REORDER"


def test_stock_status_reorder_below_threshold():
    assert stock_status(4, 5) == "REORDER"


def test_stock_status_negative_values_raise_error():
    with pytest.raises(ValueError, match="quantities cannot be negative"):
        stock_status(-1, 5)

    with pytest.raises(ValueError, match="quantities cannot be negative"):
        stock_status(1, -5)


def test_format_item_invalid_name_raises_value_error():
    with pytest.raises(ValueError, match="name required"):
        format_item("   ", "INV-1234", 1)


def test_format_item_invalid_sku_raises_value_error():
    with pytest.raises(ValueError, match="invalid sku"):
        format_item("Keyboard", "INV-12", 1)


def test_format_item_negative_quantity_raises_value_error():
    with pytest.raises(ValueError, match="quantity cannot be negative"):
        format_item("Keyboard", "INV-1234", -1)
