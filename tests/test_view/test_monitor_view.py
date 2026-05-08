"""Tests for MonitorView - REJECTED orders must be excluded."""
import pytest
from datetime import datetime
from app.view.monitor_view import MonitorView
from app.view.base_view import BaseView
from app.model.order import Order
from app.model.enums import OrderStatus


def make_order(order_no: str, status: OrderStatus) -> Order:
    return Order(
        order_no=order_no,
        sample_id="S-001",
        customer_name="Test Corp",
        quantity=5,
        status=status,
        created_at=datetime(2024, 1, 1),
    )


class TestMonitorView:
    def test_monitor_view_is_base_view(self):
        view = MonitorView()
        assert isinstance(view, BaseView)

    def test_display_none_returns_str(self):
        view = MonitorView()
        result = view.display(None)
        assert isinstance(result, str)

    def test_display_empty_list_returns_str(self):
        view = MonitorView()
        result = view.display([])
        assert isinstance(result, str)

    def test_display_excludes_rejected(self):
        view = MonitorView()
        orders = [
            make_order("ORD-20240101-0001", OrderStatus.RESERVED),
            make_order("ORD-20240101-0002", OrderStatus.REJECTED),
            make_order("ORD-20240101-0003", OrderStatus.CONFIRMED),
        ]
        result = view.display(orders)
        assert "ORD-20240101-0002" not in result
        assert "ORD-20240101-0001" in result
        assert "ORD-20240101-0003" in result

    def test_display_all_rejected_shows_no_data(self):
        view = MonitorView()
        orders = [make_order("ORD-20240101-0001", OrderStatus.REJECTED)]
        result = view.display(orders)
        assert isinstance(result, str)

    def test_display_producing_included(self):
        view = MonitorView()
        orders = [make_order("ORD-20240101-0001", OrderStatus.PRODUCING)]
        result = view.display(orders)
        assert "PRODUCING" in result

    def test_display_release_included(self):
        view = MonitorView()
        orders = [make_order("ORD-20240101-0001", OrderStatus.RELEASE)]
        result = view.display(orders)
        assert "RELEASE" in result

    def test_display_non_list_returns_str(self):
        view = MonitorView()
        result = view.display("raw string")
        assert isinstance(result, str)
