"""Red: ProductionItem model tests."""
import math
import pytest
from app.model.production import ProductionItem


class TestProductionItemCalculation:
    def test_actual_qty_formula(self):
        """actual_qty = ceil(shortage / (yield_rate * 0.9))"""
        shortage = 10
        yield_rate = 0.8
        expected_actual = math.ceil(shortage / (yield_rate * 0.9))
        item = ProductionItem(
            order_no="ORD-20240101-0001",
            sample_id="S-001",
            shortage=shortage,
            yield_rate=yield_rate,
            avg_production_time=5.0,
        )
        assert item.actual_qty == expected_actual

    def test_actual_qty_exact_division(self):
        """When division is exact, ceil has no effect."""
        shortage = 9
        yield_rate = 1.0
        # 9 / (1.0 * 0.9) = 10.0 exactly → ceil = 10
        expected_actual = math.ceil(shortage / (yield_rate * 0.9))
        item = ProductionItem(
            order_no="ORD-20240101-0002",
            sample_id="S-002",
            shortage=shortage,
            yield_rate=yield_rate,
            avg_production_time=2.0,
        )
        assert item.actual_qty == expected_actual

    def test_actual_qty_rounds_up(self):
        """Fractional result must round up."""
        shortage = 1
        yield_rate = 0.9
        # 1 / (0.9 * 0.9) ≈ 1.234 → ceil = 2
        expected_actual = math.ceil(shortage / (yield_rate * 0.9))
        item = ProductionItem(
            order_no="ORD-20240101-0003",
            sample_id="S-001",
            shortage=shortage,
            yield_rate=yield_rate,
            avg_production_time=10.0,
        )
        assert item.actual_qty == expected_actual

    def test_total_time_formula(self):
        """total_time = avg_production_time * actual_qty"""
        shortage = 10
        yield_rate = 0.8
        avg_time = 5.0
        actual_qty = math.ceil(shortage / (yield_rate * 0.9))
        expected_total = avg_time * actual_qty
        item = ProductionItem(
            order_no="ORD-20240101-0001",
            sample_id="S-001",
            shortage=shortage,
            yield_rate=yield_rate,
            avg_production_time=avg_time,
        )
        assert item.total_time == pytest.approx(expected_total)

    def test_shortage_stored(self):
        item = ProductionItem(
            order_no="ORD-20240101-0001",
            sample_id="S-001",
            shortage=20,
            yield_rate=0.95,
            avg_production_time=3.0,
        )
        assert item.shortage == 20

    def test_shortage_zero_raises(self):
        with pytest.raises(ValueError, match="shortage"):
            ProductionItem(
                order_no="ORD-20240101-0001",
                sample_id="S-001",
                shortage=0,
                yield_rate=0.8,
                avg_production_time=5.0,
            )

    def test_shortage_negative_raises(self):
        with pytest.raises(ValueError, match="shortage"):
            ProductionItem(
                order_no="ORD-20240101-0001",
                sample_id="S-001",
                shortage=-5,
                yield_rate=0.8,
                avg_production_time=5.0,
            )
