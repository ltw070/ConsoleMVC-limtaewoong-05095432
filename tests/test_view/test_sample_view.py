"""Red: SampleView tests - display returns string."""
import pytest
from app.view.sample_view import SampleView
from app.view.base_view import BaseView
from app.model.sample import Sample


@pytest.fixture
def sample():
    return Sample(id="S-001", name="Alpha", avg_production_time=5.0, yield_rate=0.9, stock=100)


class TestSampleView:
    def test_sample_view_is_base_view(self):
        view = SampleView()
        assert isinstance(view, BaseView)

    def test_display_single_sample_returns_str(self, sample):
        view = SampleView()
        result = view.display(sample)
        assert isinstance(result, str)

    def test_display_single_sample_contains_id(self, sample):
        view = SampleView()
        result = view.display(sample)
        assert "S-001" in result

    def test_display_single_sample_contains_name(self, sample):
        view = SampleView()
        result = view.display(sample)
        assert "Alpha" in result

    def test_display_list_returns_str(self, sample):
        view = SampleView()
        samples = [sample, Sample(id="S-002", name="Beta", avg_production_time=3.0, yield_rate=0.8, stock=50)]
        result = view.display(samples)
        assert isinstance(result, str)

    def test_display_empty_list_returns_str(self):
        view = SampleView()
        result = view.display([])
        assert isinstance(result, str)

    def test_display_none_returns_str(self):
        view = SampleView()
        result = view.display(None)
        assert isinstance(result, str)
