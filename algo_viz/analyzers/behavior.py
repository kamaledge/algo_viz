# algo_viz/analyzers/behavior.py
"""
Behavioral analyzers for understanding function execution patterns.
"""

from typing import List, Dict, Set, Any
from collections import defaultdict


class BehaviorAnalyzer:
    """Analyzes execution behavior to understand what the function does."""

    def __init__(self, events):
        self.events = events
        self.function_calls = self._extract_calls()
        self.variable_states = self._extract_variable_states()
        self.control_flow = self._analyze_control_flow()

    def _extract_calls(self) -> List[Dict[str, Any]]:
        """Extract function call information."""
        calls = []
        call_stack = []

        for e in self.events:
            if e.event_type == "call":
                call_info = {
                    "name": e.func_name,
                    "args": e.new_value,
                    "depth": e.depth,
                    "line": e.line_no,
                    "start_event_idx": len(self.events),
                }
                call_stack.append(call_info)

            elif e.event_type == "return":
                if call_stack:
                    call = call_stack.pop()
                    call["return_value"] = e.new_value
                    call["end_event_idx"] = len(self.events)
                    calls.append(call)

        return calls

    def _extract_variable_states(self) -> Dict[str, List[Any]]:
        """Extract state changes for each variable."""
        states = defaultdict(list)

        for e in self.events:
            if e.event_type == "var_change":
                states[e.var_name].append(
                    {
                        "old": e.old_value,
                        "new": e.new_value,
                        "line": e.line_no,
                        "depth": e.depth,
                    }
                )

        return dict(states)

    def _analyze_control_flow(self) -> Dict[str, Any]:
        """Analyze control flow structure."""
        flow = {
            "max_call_depth": 0,
            "call_count": 0,
            "return_count": 0,
            "branching_points": 0,
        }

        for e in self.events:
            if e.event_type == "call":
                flow["call_count"] += 1
                flow["max_call_depth"] = max(flow["max_call_depth"], e.depth or 0)
            elif e.event_type == "return":
                flow["return_count"] += 1

        # Detect branching by looking at divergent execution paths
        lines_executed = defaultdict(set)
        for e in self.events:
            if e.event_type == "var_change":
                lines_executed[e.line_no].add(e.var_name)

        return flow

    def get_input_output(self) -> Dict[str, Any]:
        """Analyze input and output patterns."""
        io_info = {
            "inputs": {},
            "outputs": None,
            "input_types": set(),
            "output_type": None,
        }

        # Get inputs from first call
        if self.function_calls:
            first_call = self.function_calls[0]
            if isinstance(first_call.get("args"), dict):
                io_info["inputs"] = first_call["args"]
                for arg, val in first_call["args"].items():
                    io_info["input_types"].add(type(val).__name__)

            if first_call.get("return_value") is not None:
                io_info["outputs"] = first_call["return_value"]
                io_info["output_type"] = type(first_call["return_value"]).__name__

        io_info["input_types"] = list(io_info["input_types"])
        return io_info

    def get_variable_flow(self) -> Dict[str, Any]:
        """Analyze how variables flow and change."""
        flow_info = {
            "variables": [],
            "relationships": [],
        }

        for var, states in self.variable_states.items():
            var_info = {
                "name": var,
                "changes": len(states),
                "final_value": states[-1]["new"] if states else None,
                "type_changes": 0,
            }

            # Count type changes
            for i in range(1, len(states)):
                old_type = type(states[i - 1]["new"]).__name__
                new_type = type(states[i]["new"]).__name__
                if old_type != new_type:
                    var_info["type_changes"] += 1

            flow_info["variables"].append(var_info)

        return flow_info

    def get_complexity_indicators(self) -> Dict[str, Any]:
        """Analyze indicators of algorithmic complexity."""
        complexity = {
            "loop_depth": 0,
            "recursion_depth": self.control_flow["max_call_depth"],
            "branching_factor": 0,
            "data_size": 0,
        }

        # Estimate data size from list operations
        for var, states in self.variable_states.items():
            for state in states:
                if isinstance(state["new"], list):
                    complexity["data_size"] = max(
                        complexity["data_size"], len(state["new"])
                    )

        return complexity

    def get_summary(self) -> str:
        """Generate a human-readable summary of function behavior."""
        summary_parts = []

        io = self.get_input_output()
        summary_parts.append(f"Inputs: {', '.join(str(k) for k in io['inputs'].keys())}")
        summary_parts.append(f"Returns: {io['output_type']}")

        var_flow = self.get_variable_flow()
        if var_flow["variables"]:
            summary_parts.append(
                f"Variables modified: {len(var_flow['variables'])}"
            )

        complexity = self.get_complexity_indicators()
        if complexity["recursion_depth"] > 1:
            summary_parts.append(f"Recursion depth: {complexity['recursion_depth']}")
        if complexity["data_size"] > 0:
            summary_parts.append(f"Max data size: {complexity['data_size']}")

        return " | ".join(summary_parts)
