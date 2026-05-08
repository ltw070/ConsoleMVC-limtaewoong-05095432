"""Shared formatting utilities for views."""
from typing import Any


SEPARATOR = "-" * 60
DOUBLE_SEPARATOR = "=" * 60


def header(title: str) -> str:
    """Return a formatted section header string."""
    return f"\n{DOUBLE_SEPARATOR}\n  {title}\n{DOUBLE_SEPARATOR}"


def table_row(*cols: Any, widths: list[int] | None = None) -> str:
    """Format a table row from columns with optional widths."""
    if widths:
        parts = [str(c).ljust(w) for c, w in zip(cols, widths)]
    else:
        parts = [str(c) for c in cols]
    return "  " + "  ".join(parts)


def separator() -> str:
    return SEPARATOR


def no_data(message: str = "데이터가 없습니다.") -> str:
    return f"  [{message}]"
