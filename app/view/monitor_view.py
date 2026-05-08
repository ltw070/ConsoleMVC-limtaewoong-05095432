"""MonitorView: display active orders (RESERVED/PRODUCING/CONFIRMED/RELEASE, excluding REJECTED)."""
from typing import Any
from .base_view import BaseView
from .formatters import header, separator, table_row, no_data
from app.model.order import Order
from app.model.enums import OrderStatus


class MonitorView(BaseView):
    def display(self, data: Any) -> str:
        """Render a list of Orders filtered to exclude REJECTED status."""
        if data is None:
            return no_data()

        if isinstance(data, list):
            visible = [
                o for o in data
                if isinstance(o, Order) and o.status != OrderStatus.REJECTED
            ]
            if not visible:
                return no_data("모니터링할 주문이 없습니다.")
            lines = [header("주문 모니터링 (REJECTED 제외)")]
            lines.append(
                table_row("주문번호", "시료ID", "고객명", "수량", "상태",
                          widths=[22, 8, 16, 6, 12])
            )
            lines.append(separator())
            for o in visible:
                lines.append(
                    table_row(o.order_no, o.sample_id, o.customer_name,
                              o.quantity, o.status.value,
                              widths=[22, 8, 16, 6, 12])
                )
            return "\n".join(lines)

        return str(data)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)
