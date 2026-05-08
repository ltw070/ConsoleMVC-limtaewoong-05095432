"""Red: BaseView abstract interface tests."""
import pytest
from app.view.base_view import BaseView


class TestBaseViewAbstract:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            BaseView()

    def test_subclass_without_display_raises(self):
        class IncompleteView(BaseView):
            def get_input(self, prompt: str) -> str:
                return ""

        with pytest.raises(TypeError):
            IncompleteView()

    def test_subclass_without_get_input_raises(self):
        class IncompleteView(BaseView):
            def display(self, data) -> str:
                return ""

        with pytest.raises(TypeError):
            IncompleteView()

    def test_display_returns_str(self):
        class ConcreteView(BaseView):
            def display(self, data) -> str:
                return str(data)

            def get_input(self, prompt: str) -> str:
                return ""

        v = ConcreteView()
        result = v.display("hello")
        assert isinstance(result, str)

    def test_get_input_returns_str(self):
        class ConcreteView(BaseView):
            def display(self, data) -> str:
                return ""

            def get_input(self, prompt: str) -> str:
                return "test_input"

        v = ConcreteView()
        result = v.get_input("Enter: ")
        assert isinstance(result, str)
