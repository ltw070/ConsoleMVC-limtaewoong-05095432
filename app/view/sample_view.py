"""SampleView: display for Sample domain objects."""
from typing import Any
from .base_view import BaseView
from .formatters import header, separator, table_row, no_data
from app.model.sample import Sample


class SampleView(BaseView):
    def display(self, data: Any) -> str:
        """Render a Sample, a list of Samples, or a no-data message."""
        if data is None:
            return no_data()

        if isinstance(data, Sample):
            return self._render_single(data)

        if isinstance(data, list):
            if not data:
                return no_data("등록된 시료가 없습니다.")
            lines = [header("시료 목록")]
            lines.append(
                table_row("ID", "이름", "평균생산시간(min)", "수율", "재고",
                          widths=[8, 16, 18, 8, 8])
            )
            lines.append(separator())
            for s in data:
                lines.append(
                    table_row(s.id, s.name, s.avg_production_time,
                              f"{s.yield_rate:.2%}", s.stock,
                              widths=[8, 16, 18, 8, 8])
                )
            return "\n".join(lines)

        return str(data)

    def _render_single(self, s: Sample) -> str:
        lines = [
            header(f"시료 상세 - {s.id}"),
            f"  ID              : {s.id}",
            f"  이름            : {s.name}",
            f"  평균 생산시간   : {s.avg_production_time} min/ea",
            f"  수율            : {s.yield_rate:.2%}",
            f"  재고            : {s.stock} ea",
        ]
        return "\n".join(lines)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)
