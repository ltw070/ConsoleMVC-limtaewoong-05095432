"""Red: OrderStatus enum tests."""
import pytest
from app.model.enums import OrderStatus


class TestOrderStatus:
    def test_has_reserved(self):
        assert OrderStatus.RESERVED.value == "RESERVED"

    def test_has_rejected(self):
        assert OrderStatus.REJECTED.value == "REJECTED"

    def test_has_producing(self):
        assert OrderStatus.PRODUCING.value == "PRODUCING"

    def test_has_confirmed(self):
        assert OrderStatus.CONFIRMED.value == "CONFIRMED"

    def test_has_release(self):
        assert OrderStatus.RELEASE.value == "RELEASE"

    def test_exactly_five_members(self):
        assert len(OrderStatus) == 5

    def test_all_member_names(self):
        names = {s.name for s in OrderStatus}
        assert names == {"RESERVED", "REJECTED", "PRODUCING", "CONFIRMED", "RELEASE"}
