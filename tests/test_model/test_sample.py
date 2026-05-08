"""Red: Sample model tests."""
import pytest
from app.model.sample import Sample


class TestSampleIdFormat:
    def test_valid_id_format(self):
        s = Sample(id="S-001", name="Alpha", avg_production_time=10.0, yield_rate=0.95, stock=100)
        assert s.id == "S-001"

    def test_valid_id_format_max(self):
        s = Sample(id="S-999", name="Beta", avg_production_time=5.0, yield_rate=0.8, stock=50)
        assert s.id == "S-999"

    def test_invalid_id_no_prefix(self):
        with pytest.raises(ValueError, match="id"):
            Sample(id="001", name="Bad", avg_production_time=1.0, yield_rate=0.5, stock=0)

    def test_invalid_id_wrong_digits(self):
        with pytest.raises(ValueError, match="id"):
            Sample(id="S-01", name="Bad", avg_production_time=1.0, yield_rate=0.5, stock=0)

    def test_invalid_id_letters(self):
        with pytest.raises(ValueError, match="id"):
            Sample(id="S-ABC", name="Bad", avg_production_time=1.0, yield_rate=0.5, stock=0)


class TestSampleYieldRate:
    def test_yield_rate_lower_bound_exclusive(self):
        with pytest.raises(ValueError, match="yield_rate"):
            Sample(id="S-001", name="Bad", avg_production_time=1.0, yield_rate=0.0, stock=0)

    def test_yield_rate_upper_bound_inclusive(self):
        s = Sample(id="S-001", name="Good", avg_production_time=1.0, yield_rate=1.0, stock=0)
        assert s.yield_rate == 1.0

    def test_yield_rate_above_one(self):
        with pytest.raises(ValueError, match="yield_rate"):
            Sample(id="S-001", name="Bad", avg_production_time=1.0, yield_rate=1.1, stock=0)

    def test_yield_rate_negative(self):
        with pytest.raises(ValueError, match="yield_rate"):
            Sample(id="S-001", name="Bad", avg_production_time=1.0, yield_rate=-0.1, stock=0)

    def test_yield_rate_valid_midrange(self):
        s = Sample(id="S-002", name="Mid", avg_production_time=5.0, yield_rate=0.75, stock=10)
        assert s.yield_rate == 0.75


class TestSampleStock:
    def test_stock_zero_allowed(self):
        s = Sample(id="S-001", name="Zero", avg_production_time=1.0, yield_rate=0.5, stock=0)
        assert s.stock == 0

    def test_stock_negative_raises(self):
        with pytest.raises(ValueError, match="stock"):
            Sample(id="S-001", name="Bad", avg_production_time=1.0, yield_rate=0.5, stock=-1)

    def test_stock_positive_allowed(self):
        s = Sample(id="S-001", name="Pos", avg_production_time=2.0, yield_rate=0.9, stock=500)
        assert s.stock == 500


class TestSampleAvgProductionTime:
    def test_avg_production_time_positive(self):
        s = Sample(id="S-001", name="Good", avg_production_time=0.1, yield_rate=0.5, stock=0)
        assert s.avg_production_time == 0.1

    def test_avg_production_time_zero_raises(self):
        with pytest.raises(ValueError, match="avg_production_time"):
            Sample(id="S-001", name="Bad", avg_production_time=0.0, yield_rate=0.5, stock=0)

    def test_avg_production_time_negative_raises(self):
        with pytest.raises(ValueError, match="avg_production_time"):
            Sample(id="S-001", name="Bad", avg_production_time=-1.0, yield_rate=0.5, stock=0)
