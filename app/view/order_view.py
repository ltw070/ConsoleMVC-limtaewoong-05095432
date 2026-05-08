"""OrderView: display for Order domain objects."""
from typing import Any
from .base_view import BaseView
from .formatters import header, separator, table_row, no_data
from app.model.order import Order


class OrderView(BaseView):
    def display(self, data: Any) -> str:
        """Render an Order, a list of Orders, or a no-data message."""
        if data is None:
            return no_data()

        if isinstance(data, Order):
            return self._render_single(data)

        if isinstance(data, list):
            if not data:
                return no_data("주문이 없습니다.")
            lines = [header("주문 목록")]
            lines.append(
                table_row("주문번호", "시료ID", "고객명", "수량", "상태",
                          widths=[22, 8, 16, 6, 12])
            )
            lines.append(separator())
            for o in data:
                lines.append(
                    table_row(o.order_no, o.sample_id, o.customer_name,
                              o.quantity, o.status.value,
                              widths=[22, 8, 16, 6, 12])
                )
            return "\n".join(lines)

        return str(data)

    def _render_single(self, o: Order) -> str:
        lines = [
            header(f"주문 상세 - {o.order_no}"),
            f"  주문번호  : {o.order_no}",
            f"  시료 ID   : {o.sample_id}",
            f"  고객명    : {o.customer_name}",
            f"  수량      : {o.quantity} ea",
            f"  상태      : {o.status.value}",
            f"  접수일시  : {o.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)
