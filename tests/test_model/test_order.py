"""Red: Order model tests."""
import pytest
from datetime import datetime
from app.model.order import Order
from app.model.enums import OrderStatus


class TestOrderNoFormat:
    def test_valid_order_no(self):
        o = Order(
            order_no="ORD-20240101-0001",
            sample_id="S-001",
            customer_name="ACME",
            quantity=10,
            status=OrderStatus.RESERVED,
            created_at=datetime(2024, 1, 1),
        )
        assert o.order_no == "ORD-20240101-0001"

    def test_invalid_order_no_missing_prefix(self):
        with pytest.raises(ValueError, match="order_no"):
            Order(
                order_no="20240101-0001",
                sample_id="S-001",
                customer_name="ACME",
                quantity=10,
                status=OrderStatus.RESERVED,
                created_at=datetime(2024, 1, 1),
            )

    def test_invalid_order_no_short_seq(self):
        with pytest.raises(ValueError, match="order_no"):
            Order(
                order_no="ORD-20240101-001",
                sample_id="S-001",
                customer_name="ACME",
                quantity=10,
                status=OrderStatus.RESERVED,
                created_at=datetime(2024, 1, 1),
            )

    def test_invalid_order_no_wrong_date(self):
        with pytest.raises(ValueError, match="order_no"):
            Order(
                order_no="ORD-2024011-0001",
                sample_id="S-001",
                customer_name="ACME",
                quantity=10,
                status=OrderStatus.RESERVED,
                created_at=datetime(2024, 1, 1),
            )


class TestOrderQuantity:
    def test_quantity_positive(self):
        o = Order(
            order_no="ORD-20240101-0001",
            sample_id="S-001",
            customer_name="ACME",
            quantity=1,
            status=OrderStatus.RESERVED,
            created_at=datetime(2024, 1, 1),
        )
        assert o.quantity == 1

    def test_quantity_zero_raises(self):
        with pytest.raises(ValueError, match="quantity"):
            Order(
                order_no="ORD-20240101-0001",
                sample_id="S-001",
                customer_name="ACME",
                quantity=0,
                status=OrderStatus.RESERVED,
                created_at=datetime(2024, 1, 1),
            )

    def test_quantity_negative_raises(self):
        with pytest.raises(ValueError, match="quantity"):
            Order(
                order_no="ORD-20240101-0001",
                sample_id="S-001",
                customer_name="ACME",
                quantity=-5,
                status=OrderStatus.RESERVED,
                created_at=datetime(2024, 1, 1),
            )


class TestOrderStatus:
    def test_status_is_order_status_type(self):
        o = Order(
            order_no="ORD-20240101-0001",
            sample_id="S-001",
            customer_name="ACME",
            quantity=10,
            status=OrderStatus.RESERVED,
            created_at=datetime(2024, 1, 1),
        )
        assert isinstance(o.status, OrderStatus)

    def test_status_default_reserved(self):
        o = Order(
            order_no="ORD-20240101-0001",
            sample_id="S-001",
            customer_name="ACME",
            quantity=10,
            status=OrderStatus.RESERVED,
            created_at=datetime(2024, 1, 1),
        )
        assert o.status == OrderStatus.RESERVED

    def test_status_invalid_string_raises(self):
        with pytest.raises((ValueError, TypeError)):
            Order(
                order_no="ORD-20240101-0001",
                sample_id="S-001",
                customer_name="ACME",
                quantity=10,
                status="RESERVED",  # string instead of enum
                created_at=datetime(2024, 1, 1),
            )
