"""Red: OrderView tests - display returns string."""
import pytest
from datetime import datetime
from app.view.order_view import OrderView
from app.view.base_view import BaseView
from app.model.order import Order
from app.model.enums import OrderStatus


@pytest.fixture
def order():
    return Order(
        order_no="ORD-20240101-0001",
        sample_id="S-001",
        customer_name="ACME Corp",
        quantity=10,
        status=OrderStatus.RESERVED,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
    )


class TestOrderView:
    def test_order_view_is_base_view(self):
        view = OrderView()
        assert isinstance(view, BaseView)

    def test_display_single_order_returns_str(self, order):
        view = OrderView()
        result = view.display(order)
        assert isinstance(result, str)

    def test_display_contains_order_no(self, order):
        view = OrderView()
        result = view.display(order)
        assert "ORD-20240101-0001" in result

    def test_display_contains_customer_name(self, order):
        view = OrderView()
        result = view.display(order)
        assert "ACME Corp" in result

    def test_display_contains_status(self, order):
        view = OrderView()
        result = view.display(order)
        assert "RESERVED" in result

    def test_display_list_returns_str(self, order):
        view = OrderView()
        result = view.display([order])
        assert isinstance(result, str)

    def test_display_empty_list_returns_str(self):
        view = OrderView()
        result = view.display([])
        assert isinstance(result, str)

    def test_display_none_returns_str(self):
        view = OrderView()
        result = view.display(None)
        assert isinstance(result, str)
