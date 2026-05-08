"""Abstract base view."""
from abc import ABC, abstractmethod
from typing import Any


class BaseView(ABC):
    @abstractmethod
    def display(self, data: Any) -> str:
        """Format data into a displayable string. Returns str for testability."""
        ...

    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """Read a line of input from the user."""
        ...
