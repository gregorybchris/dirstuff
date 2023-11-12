from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FilterCriteria:
    min_bytes: int
    names: Optional[List[str]]
