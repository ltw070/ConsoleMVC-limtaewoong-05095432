"""Red: SampleController tests - register → list → search flow."""
import pytest
from app.controller.sample_controller import SampleController
from app.model.sample import Sample


@pytest.fixture
def ctrl():
    return SampleController()


class TestRegisterSample:
    def test_register_returns_sample(self, ctrl):
        s = ctrl.register_sample(id="S-001", name="Alpha", avg_time=5.0, yield_rate=0.9)
        assert isinstance(s, Sample)
        assert s.id == "S-001"
        assert s.name == "Alpha"

    def test_register_default_stock_zero(self, ctrl):
        s = ctrl.register_sample(id="S-001", name="Alpha", avg_time=5.0, yield_rate=0.9)
        assert s.stock == 0

    def test_register_invalid_id_raises(self, ctrl):
        with pytest.raises(ValueError):
            ctrl.register_sample(id="001", name="Bad", avg_time=1.0, yield_rate=0.5)

    def test_register_duplicate_id_raises(self, ctrl):
        ctrl.register_sample(id="S-001", name="Alpha", avg_time=5.0, yield_rate=0.9)
        with pytest.raises(ValueError, match="already"):
            ctrl.register_sample(id="S-001", name="Beta", avg_time=3.0, yield_rate=0.8)


class TestListSamples:
    def test_list_empty_initially(self, ctrl):
        result = ctrl.list_samples()
        assert result == []

    def test_list_returns_all_registered(self, ctrl):
        ctrl.register_sample(id="S-001", name="Alpha", avg_time=5.0, yield_rate=0.9)
        ctrl.register_sample(id="S-002", name="Beta", avg_time=3.0, yield_rate=0.8)
        result = ctrl.list_samples()
        assert len(result) == 2

    def test_list_returns_copy(self, ctrl):
        ctrl.register_sample(id="S-001", name="Alpha", avg_time=5.0, yield_rate=0.9)
        result = ctrl.list_samples()
        result.clear()
        assert len(ctrl.list_samples()) == 1


class TestSearchSamples:
    def test_search_by_name(self, ctrl):
        ctrl.register_sample(id="S-001", name="Alpha-X", avg_time=5.0, yield_rate=0.9)
        ctrl.register_sample(id="S-002", name="Beta-Y", avg_time=3.0, yield_rate=0.8)
        result = ctrl.search_samples("Alpha")
        assert len(result) == 1
        assert result[0].name == "Alpha-X"

    def test_search_by_id(self, ctrl):
        ctrl.register_sample(id="S-001", name="Alpha", avg_time=5.0, yield_rate=0.9)
        ctrl.register_sample(id="S-002", name="Beta", avg_time=3.0, yield_rate=0.8)
        result = ctrl.search_samples("S-002")
        assert len(result) == 1
        assert result[0].id == "S-002"

    def test_search_case_insensitive(self, ctrl):
        ctrl.register_sample(id="S-001", name="Alpha", avg_time=5.0, yield_rate=0.9)
        result = ctrl.search_samples("alpha")
        assert len(result) == 1

    def test_search_no_match_returns_empty(self, ctrl):
        ctrl.register_sample(id="S-001", name="Alpha", avg_time=5.0, yield_rate=0.9)
        result = ctrl.search_samples("XYZ")
        assert result == []
