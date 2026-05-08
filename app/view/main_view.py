"""MainView: system status dashboard and main menu."""
from typing import Any
from .base_view import BaseView
from .formatters import header, separator, no_data


class MainView(BaseView):
    MENU = (
        "  [1] 시료 관리",
        "  [2] 주문 접수",
        "  [3] 주문 승인/거절",
        "  [4] 모니터링",
        "  [5] 생산 라인",
        "  [6] 출고 처리",
        "  [0] 종료",
    )

    def display(self, data: Any) -> str:
        """Render system status summary and main menu."""
        lines = [header("S-Semi 반도체 시료 생산주문관리 시스템")]

        # System status block
        if data and isinstance(data, dict):
            lines.append("")
            lines.append("  [시스템 현황]")
            for key, val in data.items():
                lines.append(f"  • {key}: {val}")
        lines.append("")
        lines.append(separator())
        lines.append("  [메인 메뉴]")
        lines.extend(self.MENU)
        lines.append(separator())
        return "\n".join(lines)

    def get_input(self, prompt: str = "선택 > ") -> str:
        return input(prompt)
