"""Abstract base controller."""
from abc import ABC, abstractmethod


class BaseController(ABC):
    @abstractmethod
    def run(self) -> None:
        """Entry point for controller interaction loop."""
        ...
