"""Red: OrderController tests - place/approve/reject/ship flows."""
import pytest
from datetime import datetime
from app.controller.order_controller import OrderController
from app.controller.sample_controller import SampleController
from app.controller.production_controller import ProductionController
from app.model.order import Order
from app.model.enums import OrderStatus


@pytest.fixture
def sample_ctrl():
    ctrl = SampleController()
    ctrl.register_sample(id="S-001", name="Alpha", avg_time=5.0, yield_rate=0.9)
    ctrl.register_sample(id="S-002", name="Beta", avg_time=3.0, yield_rate=0.8)
    return ctrl


@pytest.fixture
def prod_ctrl():
    return ProductionController()


@pytest.fixture
def ctrl(sample_ctrl, prod_ctrl):
    return OrderController(sample_ctrl=sample_ctrl, prod_ctrl=prod_ctrl)


class TestPlaceOrder:
    def test_place_order_returns_order(self, ctrl):
        order = ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        assert isinstance(order, Order)

    def test_place_order_status_reserved(self, ctrl):
        order = ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        assert order.status == OrderStatus.RESERVED

    def test_place_order_no_format(self, ctrl):
        order = ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        import re
        assert re.fullmatch(r"ORD-\d{8}-\d{4}", order.order_no)

    def test_place_order_unknown_sample_raises(self, ctrl):
        with pytest.raises(ValueError, match="sample"):
            ctrl.place_order(sample_id="S-999", customer="ACME", qty=10)

    def test_place_order_sequential_order_nos(self, ctrl):
        o1 = ctrl.place_order(sample_id="S-001", customer="ACME", qty=5)
        o2 = ctrl.place_order(sample_id="S-001", customer="Corp", qty=3)
        assert o1.order_no != o2.order_no


class TestListReserved:
    def test_list_reserved_empty_initially(self, ctrl):
        assert ctrl.list_reserved() == []

    def test_list_reserved_returns_reserved_orders(self, ctrl):
        ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        ctrl.place_order(sample_id="S-002", customer="Corp", qty=5)
        result = ctrl.list_reserved()
        assert len(result) == 2
        assert all(o.status == OrderStatus.RESERVED for o in result)


class TestApproveOrderSufficientStock:
    def test_approve_with_sufficient_stock_confirmed(self, ctrl, sample_ctrl):
        # Set stock high enough
        sample = sample_ctrl.list_samples()[0]
        object.__setattr__(sample, "stock", 100)
        order = ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        approved = ctrl.approve_order(order.order_no)
        assert approved.status == OrderStatus.CONFIRMED

    def test_approve_reduces_stock(self, ctrl, sample_ctrl):
        sample = sample_ctrl.list_samples()[0]
        object.__setattr__(sample, "stock", 50)
        order = ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        ctrl.approve_order(order.order_no)
        assert sample.stock == 40


class TestApproveOrderInsufficientStock:
    def test_approve_with_no_stock_goes_producing(self, ctrl, sample_ctrl):
        # stock is 0 by default
        order = ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        approved = ctrl.approve_order(order.order_no)
        assert approved.status == OrderStatus.PRODUCING

    def test_approve_partial_stock_goes_producing(self, ctrl, sample_ctrl):
        sample = sample_ctrl.list_samples()[0]
        object.__setattr__(sample, "stock", 5)
        order = ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        approved = ctrl.approve_order(order.order_no)
        assert approved.status == OrderStatus.PRODUCING

    def test_approve_insufficient_creates_production_item(self, ctrl, sample_ctrl, prod_ctrl):
        order = ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        ctrl.approve_order(order.order_no)
        queue = prod_ctrl.get_queue()
        assert len(queue) == 1
        assert queue[0].order_no == order.order_no


class TestRejectOrder:
    def test_reject_sets_rejected_status(self, ctrl):
        order = ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        rejected = ctrl.reject_order(order.order_no)
        assert rejected.status == OrderStatus.REJECTED

    def test_reject_nonexistent_raises(self, ctrl):
        with pytest.raises(ValueError, match="order"):
            ctrl.reject_order("ORD-20240101-9999")


class TestShipOrder:
    def test_ship_confirmed_becomes_release(self, ctrl, sample_ctrl):
        sample = sample_ctrl.list_samples()[0]
        object.__setattr__(sample, "stock", 100)
        order = ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        ctrl.approve_order(order.order_no)
        shipped = ctrl.ship_order(order.order_no)
        assert shipped.status == OrderStatus.RELEASE

    def test_ship_non_confirmed_raises(self, ctrl):
        order = ctrl.place_order(sample_id="S-001", customer="ACME", qty=10)
        with pytest.raises(ValueError, match="CONFIRMED"):
            ctrl.ship_order(order.order_no)
