"""Sample domain model."""
from dataclasses import dataclass, field
from .validators import validate_sample_id, validate_yield_rate, validate_non_negative_int, validate_positive_float


@dataclass
class Sample:
    id: str
    name: str
    avg_production_time: float   # unit: min/ea, must be positive
    yield_rate: float            # range: 0 < yield_rate <= 1
    stock: int                   # unit: ea, must be >= 0

    def __post_init__(self):
        validate_sample_id(self.id)
        validate_positive_float(self.avg_production_time, "avg_production_time")
        validate_yield_rate(self.yield_rate)
        validate_non_negative_int(self.stock, "stock")
