"""OrderController: manages order placement, approval, rejection, and shipment."""
from datetime import datetime
from .base_controller import BaseController
from .sample_controller import SampleController
from .production_controller import ProductionController
from app.model.order import Order
from app.model.enums import OrderStatus
from app.model.production import ProductionItem


class OrderController(BaseController):
    def __init__(
        self,
        sample_ctrl: SampleController,
        prod_ctrl: ProductionController,
    ):
        self._sample_ctrl = sample_ctrl
        self._prod_ctrl = prod_ctrl
        self._orders: dict[str, Order] = {}
        self._seq: int = 0

    def run(self) -> None:
        """Interactive loop placeholder - used by main.py."""
        pass

    def _next_order_no(self) -> str:
        """Generate the next order number in ORD-YYYYMMDD-XXXX format."""
        self._seq += 1
        date_str = datetime.now().strftime("%Y%m%d")
        return f"ORD-{date_str}-{self._seq:04d}"

    def place_order(self, sample_id: str, customer: str, qty: int) -> Order:
        """Create a new order in RESERVED status.

        Raises ValueError if the sample does not exist.
        """
        sample = self._sample_ctrl.get_sample(sample_id)
        if sample is None:
            raise ValueError(f"Unknown sample id: {sample_id!r}")
        order = Order(
            order_no=self._next_order_no(),
            sample_id=sample_id,
            customer_name=customer,
            quantity=qty,
            status=OrderStatus.RESERVED,
            created_at=datetime.now(),
        )
        self._orders[order.order_no] = order
        return order

    def list_reserved(self) -> list[Order]:
        """Return all orders with RESERVED status."""
        return [o for o in self._orders.values() if o.status == OrderStatus.RESERVED]

    def approve_order(self, order_no: str) -> Order:
        """Approve an order.

        - If stock >= quantity: status → CONFIRMED, deduct stock.
        - If stock < quantity: status → PRODUCING, create ProductionItem and enqueue.

        Raises ValueError if the order does not exist.
        """
        order = self._get_order(order_no)
        sample = self._sample_ctrl.get_sample(order.sample_id)
        if sample is None:
            raise ValueError(f"Sample {order.sample_id!r} not found")

        if sample.stock >= order.quantity:
            # Sufficient stock — confirm immediately
            object.__setattr__(sample, "stock", sample.stock - order.quantity)
            object.__setattr__(order, "status", OrderStatus.CONFIRMED)
        else:
            # Insufficient stock — send to production
            shortage = order.quantity - sample.stock
            # Use up whatever stock exists
            object.__setattr__(sample, "stock", 0)
            prod_item = ProductionItem(
                order_no=order.order_no,
                sample_id=order.sample_id,
                shortage=shortage,
                yield_rate=sample.yield_rate,
                avg_production_time=sample.avg_production_time,
            )
            self._prod_ctrl.enqueue(prod_item)
            object.__setattr__(order, "status", OrderStatus.PRODUCING)

        return order

    def reject_order(self, order_no: str) -> Order:
        """Reject an order (status → REJECTED).

        Raises ValueError if the order does not exist.
        """
        order = self._get_order(order_no)
        object.__setattr__(order, "status", OrderStatus.REJECTED)
        return order

    def ship_order(self, order_no: str) -> Order:
        """Ship an order (CONFIRMED → RELEASE).

        Raises ValueError if the order is not in CONFIRMED status.
        """
        order = self._get_order(order_no)
        if order.status != OrderStatus.CONFIRMED:
            raise ValueError(
                f"Order {order_no!r} must be in CONFIRMED status to ship, "
                f"but is {order.status.value!r}"
            )
        object.__setattr__(order, "status", OrderStatus.RELEASE)
        return order

    def _get_order(self, order_no: str) -> Order:
        """Retrieve an order by number or raise ValueError."""
        order = self._orders.get(order_no)
        if order is None:
            raise ValueError(f"No order found with order_no: {order_no!r}")
        return order
