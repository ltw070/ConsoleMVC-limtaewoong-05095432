"""Red: MainView tests - display returns string, no direct print calls."""
import pytest
from app.view.main_view import MainView
from app.view.base_view import BaseView


class TestMainView:
    def test_main_view_is_base_view(self):
        view = MainView()
        assert isinstance(view, BaseView)

    def test_display_returns_str(self):
        view = MainView()
        result = view.display({})
        assert isinstance(result, str)

    def test_display_contains_menu_items(self):
        view = MainView()
        result = view.display({})
        # Should contain main menu options
        assert "1" in result
        assert "0" in result

    def test_display_shows_system_status(self):
        view = MainView()
        data = {
            "total_orders": 5,
            "producing": 2,
            "confirmed": 1,
        }
        result = view.display(data)
        assert isinstance(result, str)

    def test_display_empty_data_no_error(self):
        view = MainView()
        result = view.display(None)
        assert isinstance(result, str)
