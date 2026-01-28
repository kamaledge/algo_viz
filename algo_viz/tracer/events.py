# algo_viz/tracer/events.py

from dataclasses import dataclass
from typing import Any

@dataclass
class Event:
    event_type: str          # "line", "var_change", "call", "return"
    line_no: int | None
    func_name: str | None
    var_name: str | None
    old_value: Any
    new_value: Any
    depth: int | None = None
