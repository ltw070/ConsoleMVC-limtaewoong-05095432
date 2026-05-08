"""SampleController: manages Sample registration and lookup."""
from .base_controller import BaseController
from app.model.sample import Sample


class SampleController(BaseController):
    def __init__(self):
        self._samples: dict[str, Sample] = {}

    def run(self) -> None:
        """Interactive loop placeholder - used by main.py."""
        pass

    def register_sample(
        self,
        id: str,
        name: str,
        avg_time: float,
        yield_rate: float,
        stock: int = 0,
    ) -> Sample:
        """Create and register a new Sample.

        Raises ValueError if the id already exists or if any field is invalid.
        """
        if id in self._samples:
            raise ValueError(f"Sample with id {id!r} already exists")
        sample = Sample(
            id=id,
            name=name,
            avg_production_time=avg_time,
            yield_rate=yield_rate,
            stock=stock,
        )
        self._samples[id] = sample
        return sample

    def list_samples(self) -> list[Sample]:
        """Return a shallow copy of all registered samples."""
        return list(self._samples.values())

    def search_samples(self, keyword: str) -> list[Sample]:
        """Return samples whose id or name contains keyword (case-insensitive)."""
        kw = keyword.lower()
        return [
            s for s in self._samples.values()
            if kw in s.id.lower() or kw in s.name.lower()
        ]

    def get_sample(self, sample_id: str) -> Sample | None:
        """Return the sample with the given id, or None if not found."""
        return self._samples.get(sample_id)
