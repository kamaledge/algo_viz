# algo_viz/tracer/events.py

from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Event:
    event_type: str          # "line", "var_change", "call", "return"
    line_no: Optional[int]
    func_name: Optional[str]
    var_name: Optional[str]
    old_value: Any
    new_value: Any
    depth: Optional[int] = None
