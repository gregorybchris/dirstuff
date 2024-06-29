from dataclasses import dataclass


@dataclass
class FilterCriteria:
    """Criteria to use when filtering directories."""

    min_bytes: int
