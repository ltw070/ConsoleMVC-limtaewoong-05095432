"""Tests for ProductionView."""
import pytest
from app.view.production_view import ProductionView
from app.view.base_view import BaseView
from app.model.production import ProductionItem


@pytest.fixture
def item():
    return ProductionItem(
        order_no="ORD-20240101-0001",
        sample_id="S-001",
        shortage=10,
        yield_rate=0.9,
        avg_production_time=5.0,
    )


class TestProductionView:
    def test_production_view_is_base_view(self):
        view = ProductionView()
        assert isinstance(view, BaseView)

    def test_display_none_returns_str(self):
        view = ProductionView()
        result = view.display(None)
        assert isinstance(result, str)

    def test_display_single_item_returns_str(self, item):
        view = ProductionView()
        result = view.display(item)
        assert isinstance(result, str)

    def test_display_single_item_contains_order_no(self, item):
        view = ProductionView()
        result = view.display(item)
        assert "ORD-20240101-0001" in result

    def test_display_list_returns_str(self, item):
        view = ProductionView()
        result = view.display([item])
        assert isinstance(result, str)

    def test_display_empty_list_returns_str(self):
        view = ProductionView()
        result = view.display([])
        assert isinstance(result, str)

    def test_display_list_contains_order_no(self, item):
        view = ProductionView()
        result = view.display([item])
        assert "ORD-20240101-0001" in result

    def test_display_non_list_non_item_returns_str(self):
        view = ProductionView()
        result = view.display("raw")
        assert isinstance(result, str)
