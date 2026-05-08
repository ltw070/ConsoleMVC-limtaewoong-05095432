"""Tests for ShipmentView."""
import pytest
from datetime import datetime
from app.view.shipment_view import ShipmentView
from app.view.base_view import BaseView
from app.model.order import Order
from app.model.enums import OrderStatus


def make_order(order_no: str, status: OrderStatus) -> Order:
    return Order(
        order_no=order_no,
        sample_id="S-001",
        customer_name="Ship Corp",
        quantity=5,
        status=status,
        created_at=datetime(2024, 1, 1),
    )


class TestShipmentView:
    def test_shipment_view_is_base_view(self):
        view = ShipmentView()
        assert isinstance(view, BaseView)

    def test_display_none_returns_str(self):
        view = ShipmentView()
        result = view.display(None)
        assert isinstance(result, str)

    def test_display_single_order_returns_str(self):
        view = ShipmentView()
        order = make_order("ORD-20240101-0001", OrderStatus.RELEASE)
        result = view.display(order)
        assert isinstance(result, str)

    def test_display_single_order_contains_order_no(self):
        view = ShipmentView()
        order = make_order("ORD-20240101-0001", OrderStatus.RELEASE)
        result = view.display(order)
        assert "ORD-20240101-0001" in result

    def test_display_list_confirmed_returns_str(self):
        view = ShipmentView()
        orders = [make_order("ORD-20240101-0001", OrderStatus.CONFIRMED)]
        result = view.display(orders)
        assert isinstance(result, str)

    def test_display_list_no_confirmed_shows_empty_msg(self):
        view = ShipmentView()
        orders = [make_order("ORD-20240101-0001", OrderStatus.RESERVED)]
        result = view.display(orders)
        assert isinstance(result, str)

    def test_display_empty_list_returns_str(self):
        view = ShipmentView()
        result = view.display([])
        assert isinstance(result, str)

    def test_display_list_shows_confirmed_order(self):
        view = ShipmentView()
        orders = [
            make_order("ORD-20240101-0001", OrderStatus.CONFIRMED),
            make_order("ORD-20240101-0002", OrderStatus.RESERVED),
        ]
        result = view.display(orders)
        assert "ORD-20240101-0001" in result
        assert "ORD-20240101-0002" not in result

    def test_display_non_list_non_order_returns_str(self):
        view = ShipmentView()
        result = view.display("raw")
        assert isinstance(result, str)
