"""Red: ProductionController tests - FIFO queue, complete_production."""
import pytest
from app.controller.production_controller import ProductionController
from app.model.production import ProductionItem
from app.model.enums import OrderStatus


@pytest.fixture
def ctrl():
    return ProductionController()


def make_item(order_no: str, sample_id: str = "S-001") -> ProductionItem:
    return ProductionItem(
        order_no=order_no,
        sample_id=sample_id,
        shortage=10,
        yield_rate=0.9,
        avg_production_time=5.0,
    )


class TestGetCurrent:
    def test_get_current_empty_returns_none(self, ctrl):
        assert ctrl.get_current() is None

    def test_get_current_returns_first_item(self, ctrl):
        item = make_item("ORD-20240101-0001")
        ctrl.enqueue(item)
        current = ctrl.get_current()
        assert current is not None
        assert current.order_no == "ORD-20240101-0001"


class TestGetQueue:
    def test_get_queue_empty_initially(self, ctrl):
        assert ctrl.get_queue() == []

    def test_get_queue_returns_all_items(self, ctrl):
        ctrl.enqueue(make_item("ORD-20240101-0001"))
        ctrl.enqueue(make_item("ORD-20240101-0002"))
        queue = ctrl.get_queue()
        assert len(queue) == 2

    def test_get_queue_fifo_order(self, ctrl):
        ctrl.enqueue(make_item("ORD-20240101-0001"))
        ctrl.enqueue(make_item("ORD-20240101-0002"))
        ctrl.enqueue(make_item("ORD-20240101-0003"))
        queue = ctrl.get_queue()
        order_nos = [item.order_no for item in queue]
        assert order_nos == [
            "ORD-20240101-0001",
            "ORD-20240101-0002",
            "ORD-20240101-0003",
        ]

    def test_get_queue_returns_copy(self, ctrl):
        ctrl.enqueue(make_item("ORD-20240101-0001"))
        queue = ctrl.get_queue()
        queue.clear()
        assert len(ctrl.get_queue()) == 1


class TestCompleteProduction:
    def test_complete_production_removes_from_queue(self, ctrl):
        item = make_item("ORD-20240101-0001")
        ctrl.enqueue(item)
        ctrl.complete_production("ORD-20240101-0001")
        assert ctrl.get_current() is None

    def test_complete_production_fifo_advances(self, ctrl):
        ctrl.enqueue(make_item("ORD-20240101-0001"))
        ctrl.enqueue(make_item("ORD-20240101-0002"))
        ctrl.complete_production("ORD-20240101-0001")
        current = ctrl.get_current()
        assert current is not None
        assert current.order_no == "ORD-20240101-0002"

    def test_complete_production_nonexistent_raises(self, ctrl):
        with pytest.raises(ValueError, match="order"):
            ctrl.complete_production("ORD-20240101-9999")

    def test_complete_production_non_head_raises(self, ctrl):
        """Only the head of the FIFO queue can be completed."""
        ctrl.enqueue(make_item("ORD-20240101-0001"))
        ctrl.enqueue(make_item("ORD-20240101-0002"))
        with pytest.raises(ValueError, match="head"):
            ctrl.complete_production("ORD-20240101-0002")
