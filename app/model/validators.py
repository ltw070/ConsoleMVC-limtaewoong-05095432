"""Shared validation utilities for domain models."""
import re


def validate_sample_id(value: str) -> str:
    """Validate sample id format: S-\\d{3} (e.g. S-001)."""
    if not re.fullmatch(r"S-\d{3}", value):
        raise ValueError(f"id must match S-NNN format (e.g. S-001), got: {value!r}")
    return value


def validate_order_no(value: str) -> str:
    """Validate order_no format: ORD-YYYYMMDD-XXXX (4-digit sequence)."""
    if not re.fullmatch(r"ORD-\d{8}-\d{4}", value):
        raise ValueError(
            f"order_no must match ORD-YYYYMMDD-XXXX format, got: {value!r}"
        )
    return value


def validate_positive_float(value: float, field_name: str) -> float:
    """Validate that a float is strictly positive."""
    if value <= 0:
        raise ValueError(f"{field_name} must be positive (> 0), got: {value}")
    return value


def validate_yield_rate(value: float) -> float:
    """Validate yield_rate is in range (0, 1]."""
    if not (0 < value <= 1):
        raise ValueError(f"yield_rate must be in range (0, 1], got: {value}")
    return value


def validate_non_negative_int(value: int, field_name: str) -> int:
    """Validate that an integer is non-negative (>= 0)."""
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0, got: {value}")
    return value


def validate_positive_int(value: int, field_name: str) -> int:
    """Validate that an integer is strictly positive (> 0)."""
    if value <= 0:
        raise ValueError(f"{field_name} must be > 0, got: {value}")
    return value
