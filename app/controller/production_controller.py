"""ProductionController: manages the FIFO production queue."""
from collections import deque
from .base_controller import BaseController
from app.model.production import ProductionItem


class ProductionController(BaseController):
    def __init__(self):
        self._queue: deque[ProductionItem] = deque()

    def run(self) -> None:
        """Interactive loop placeholder - used by main.py."""
        pass

    def enqueue(self, item: ProductionItem) -> None:
        """Add a ProductionItem to the end of the FIFO queue."""
        self._queue.append(item)

    def get_current(self) -> ProductionItem | None:
        """Return the head of the queue (currently producing), or None if empty."""
        return self._queue[0] if self._queue else None

    def get_queue(self) -> list[ProductionItem]:
        """Return a copy of the production queue in FIFO order."""
        return list(self._queue)

    def complete_production(self, order_no: str) -> None:
        """Mark the head item as complete and remove it from the queue.

        Raises ValueError if order_no is not in the queue or is not the head.
        """
        if not self._queue:
            raise ValueError(f"No production order found: {order_no!r}")
        head = self._queue[0]
        if head.order_no != order_no:
            # Check if it exists elsewhere in the queue
            found = any(item.order_no == order_no for item in self._queue)
            if found:
                raise ValueError(
                    f"Order {order_no!r} is not the head of the queue; "
                    "only the current (head) production item can be completed"
                )
            raise ValueError(f"No production order found: {order_no!r}")
        self._queue.popleft()
