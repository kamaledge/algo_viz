from dataclasses import dataclass
from typing import Any

@dataclass
class DPUpdateEvent:
    table: str
    index: Any  # Can be int, str (variable name), or expression
    inputs: dict
    result: Any  # Can be int, float, or other numeric types
    line_no: int
