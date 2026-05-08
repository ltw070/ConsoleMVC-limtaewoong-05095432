"""Red: BaseController abstract interface tests."""
import pytest
from app.controller.base_controller import BaseController


class TestBaseControllerAbstract:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            BaseController()

    def test_subclass_without_run_raises(self):
        class IncompleteController(BaseController):
            pass

        with pytest.raises(TypeError):
            IncompleteController()

    def test_subclass_with_run_can_instantiate(self):
        class ConcreteController(BaseController):
            def run(self) -> None:
                pass

        ctrl = ConcreteController()
        assert ctrl is not None

    def test_run_returns_none(self):
        class ConcreteController(BaseController):
            def run(self) -> None:
                return None

        ctrl = ConcreteController()
        result = ctrl.run()
        assert result is None
