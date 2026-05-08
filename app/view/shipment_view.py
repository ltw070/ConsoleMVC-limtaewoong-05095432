"""ShipmentView: display for shipment (출고) processing."""
from typing import Any
from .base_view import BaseView
from .formatters import header, separator, table_row, no_data
from app.model.order import Order
from app.model.enums import OrderStatus


class ShipmentView(BaseView):
    def display(self, data: Any) -> str:
        """Render CONFIRMED orders ready for shipment, or a shipped Order."""
        if data is None:
            return no_data()

        if isinstance(data, Order):
            return self._render_single(data)

        if isinstance(data, list):
            confirmed = [
                o for o in data
                if isinstance(o, Order) and o.status == OrderStatus.CONFIRMED
            ]
            if not confirmed:
                return no_data("출고 대기 주문이 없습니다.")
            lines = [header("출고 대기 목록 (CONFIRMED)")]
            lines.append(
                table_row("주문번호", "시료ID", "고객명", "수량",
                          widths=[22, 8, 16, 6])
            )
            lines.append(separator())
            for o in confirmed:
                lines.append(
                    table_row(o.order_no, o.sample_id, o.customer_name,
                              o.quantity, widths=[22, 8, 16, 6])
                )
            return "\n".join(lines)

        return str(data)

    def _render_single(self, o: Order) -> str:
        lines = [
            header(f"출고 처리 완료 - {o.order_no}"),
            f"  주문번호 : {o.order_no}",
            f"  고객명   : {o.customer_name}",
            f"  상태     : {o.status.value}",
        ]
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)
