"""ProductionView: display for ProductionItem objects (production queue)."""
from typing import Any
from .base_view import BaseView
from .formatters import header, separator, table_row, no_data
from app.model.production import ProductionItem


class ProductionView(BaseView):
    def display(self, data: Any) -> str:
        """Render a ProductionItem or list of ProductionItems."""
        if data is None:
            return no_data()

        if isinstance(data, ProductionItem):
            return self._render_single(data)

        if isinstance(data, list):
            if not data:
                return no_data("생산 대기 항목이 없습니다.")
            lines = [header("생산 대기 큐 (FIFO)")]
            lines.append(
                table_row("순위", "주문번호", "시료ID", "부족분", "실생산량", "총시간(min)",
                          widths=[4, 22, 8, 8, 10, 12])
            )
            lines.append(separator())
            for i, item in enumerate(data, 1):
                lines.append(
                    table_row(i, item.order_no, item.sample_id,
                              item.shortage, item.actual_qty,
                              f"{item.total_time:.1f}",
                              widths=[4, 22, 8, 8, 10, 12])
                )
            return "\n".join(lines)

        return str(data)

    def _render_single(self, item: ProductionItem) -> str:
        lines = [
            header(f"생산 항목 - {item.order_no}"),
            f"  주문번호    : {item.order_no}",
            f"  시료 ID     : {item.sample_id}",
            f"  부족분      : {item.shortage} ea",
            f"  실 생산량   : {item.actual_qty} ea",
            f"  총 생산시간 : {item.total_time:.1f} min",
        ]
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)
