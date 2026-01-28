# algo_viz/detectors/generic.py
"""
Generic pattern detectors for analyzing function behavior.
These detectors go beyond specific algorithms to identify general programming patterns.
"""

from typing import List, Dict, Set, Any
from collections import defaultdict


class GenericPatternDetector:
    """Detects generic programming patterns in function execution."""

    def __init__(self, events):
        self.events = events
        self.patterns = {}
        self._analyze()

    def _analyze(self):
        """Analyze events and detect patterns."""
        self.patterns = {
            "loops": self._detect_loops(),
            "conditionals": self._detect_conditionals(),
            "data_structures": self._detect_data_structures(),
            "arithmetic": self._detect_arithmetic_operations(),
            "comparisons": self._detect_comparisons(),
            "variable_mutations": self._detect_mutations(),
            "function_calls": self._detect_function_calls(),
            "data_transformations": self._detect_data_transformations(),
        }

    def _detect_loops(self) -> Dict[str, Any]:
        """Detect loop-like behavior: repeated variable changes at same depth."""
        loop_patterns = {
            "detected": False,
            "loop_vars": [],
            "iteration_count": 0,
        }

        # Track when variables change repeatedly
        var_change_sequences = defaultdict(list)

        for e in self.events:
            if e.event_type == "var_change":
                var_change_sequences[e.var_name].append(e)

        # Variables that change multiple times suggest loops
        loop_vars = [
            var for var, changes in var_change_sequences.items() if len(changes) > 2
        ]

        if loop_vars:
            loop_patterns["detected"] = True
            loop_patterns["loop_vars"] = loop_vars
            # Count approximate iterations by looking at loop variable changes
            if loop_vars:
                loop_patterns["iteration_count"] = len(var_change_sequences[loop_vars[0]])

        return loop_patterns

    def _detect_conditionals(self) -> Dict[str, Any]:
        """Detect conditional branching by analyzing variable changes and returns."""
        conditional_patterns = {
            "detected": False,
            "branches": 0,
            "early_returns": 0,
            "has_branches": False,
        }

        # Count early returns (returns not at max depth)
        max_depth = 0
        for e in self.events:
            if e.event_type == "call":
                max_depth = max(max_depth, e.depth or 0)

        early_returns = sum(
            1 for e in self.events
            if e.event_type == "return" and (e.depth or 0) < max_depth
        )

        if early_returns > 0:
            conditional_patterns["detected"] = True
            conditional_patterns["early_returns"] = early_returns
            conditional_patterns["has_branches"] = True

        # Also detect variable divergence - when a variable can take different paths
        var_paths = defaultdict(set)
        for e in self.events:
            if e.event_type == "var_change":
                var_paths[e.var_name].add((e.new_value, e.line_no))

        branches = sum(1 for vars_set in var_paths.values() if len(vars_set) > 1)
        if branches > 0:
            conditional_patterns["detected"] = True
            conditional_patterns["branches"] = branches

        return conditional_patterns

    def _detect_data_structures(self) -> Dict[str, Any]:
        """Detect use of different data structures."""
        ds_patterns = {
            "list_operations": 0,
            "dict_operations": 0,
            "set_operations": 0,
            "string_operations": 0,
            "detected_types": [],
        }

        for e in self.events:
            if e.event_type == "var_change":
                # Check for list operations
                if "[" in (e.var_name or "") and "]" in (e.var_name or ""):
                    ds_patterns["list_operations"] += 1

                # Check types in events
                if isinstance(e.new_value, list):
                    if "list" not in ds_patterns["detected_types"]:
                        ds_patterns["detected_types"].append("list")
                elif isinstance(e.new_value, dict):
                    if "dict" not in ds_patterns["detected_types"]:
                        ds_patterns["detected_types"].append("dict")
                    ds_patterns["dict_operations"] += 1
                elif isinstance(e.new_value, set):
                    if "set" not in ds_patterns["detected_types"]:
                        ds_patterns["detected_types"].append("set")
                    ds_patterns["set_operations"] += 1
                elif isinstance(e.new_value, str):
                    if "string" not in ds_patterns["detected_types"]:
                        ds_patterns["detected_types"].append("string")
                    ds_patterns["string_operations"] += 1

        return ds_patterns

    def _detect_arithmetic_operations(self) -> Dict[str, Any]:
        """Detect arithmetic and numeric operations."""
        arith_patterns = {
            "numeric_ops": 0,
            "increment_ops": 0,
            "decrement_ops": 0,
            "detected": False,
        }

        for e in self.events:
            if e.event_type == "var_change":
                if isinstance(e.old_value, (int, float)) and isinstance(
                    e.new_value, (int, float)
                ):
                    arith_patterns["numeric_ops"] += 1

                    delta = e.new_value - e.old_value
                    if delta == 1:
                        arith_patterns["increment_ops"] += 1
                    elif delta == -1:
                        arith_patterns["decrement_ops"] += 1

        if arith_patterns["numeric_ops"] > 0:
            arith_patterns["detected"] = True

        return arith_patterns

    def _detect_comparisons(self) -> Dict[str, Any]:
        """Detect comparison operations via variable changes."""
        comp_patterns = {
            "comparison_chains": 0,
            "values_compared": set(),
        }

        # Track sequences of comparisons
        for e in self.events:
            if e.event_type == "var_change":
                if isinstance(e.new_value, bool):
                    comp_patterns["comparison_chains"] += 1
                # Track all values involved in changes
                comp_patterns["values_compared"].add(e.new_value)

        comp_patterns["values_compared"] = len(comp_patterns["values_compared"])
        return comp_patterns

    def _detect_mutations(self) -> Dict[str, Any]:
        """Detect variable mutations and state changes."""
        mutation_patterns = {
            "total_mutations": 0,
            "mutated_vars": set(),
            "mutation_frequency": {},
        }

        for e in self.events:
            if e.event_type == "var_change":
                mutation_patterns["total_mutations"] += 1
                mutation_patterns["mutated_vars"].add(e.var_name)

                mutation_patterns["mutation_frequency"][e.var_name] = (
                    mutation_patterns["mutation_frequency"].get(e.var_name, 0) + 1
                )

        mutation_patterns["mutated_vars"] = list(mutation_patterns["mutated_vars"])
        return mutation_patterns

    def _detect_function_calls(self) -> Dict[str, Any]:
        """Detect recursive and nested function calls."""
        call_patterns = {
            "total_calls": 0,
            "recursive": False,
            "max_depth": 0,
            "call_stack": [],
        }

        call_stack = []
        max_depth = 0

        for e in self.events:
            if e.event_type == "call":
                call_stack.append(e.func_name)
                call_patterns["total_calls"] += 1
                max_depth = max(max_depth, len(call_stack))

                # Check for recursion
                if e.func_name in call_stack[:-1]:
                    call_patterns["recursive"] = True

            elif e.event_type == "return" and call_stack:
                call_stack.pop()

        call_patterns["max_depth"] = max_depth
        return call_patterns

    def _detect_data_transformations(self) -> Dict[str, Any]:
        """Detect transformations of data types and values."""
        transform_patterns = {
            "type_conversions": 0,
            "value_transformations": 0,
            "transformation_pairs": [],
        }

        for e in self.events:
            if e.event_type == "var_change":
                old_type = type(e.old_value).__name__
                new_type = type(e.new_value).__name__

                if old_type != new_type:
                    transform_patterns["type_conversions"] += 1
                    transform_patterns["transformation_pairs"].append(
                        (old_type, new_type)
                    )

                # Any significant value change
                if e.old_value != e.new_value:
                    transform_patterns["value_transformations"] += 1

        return transform_patterns

    def get_summary(self) -> Dict[str, Any]:
        """Get a human-readable summary of detected patterns."""
        summary = {}

        for pattern_name, pattern_data in self.patterns.items():
            if isinstance(pattern_data, dict) and pattern_data.get("detected"):
                summary[pattern_name] = pattern_data

        # Also include high-activity patterns
        if self.patterns["loops"]["detected"]:
            summary["loops"] = self.patterns["loops"]

        if self.patterns["conditionals"]["detected"]:
            summary["conditionals"] = self.patterns["conditionals"]

        if self.patterns["data_structures"]["detected_types"]:
            summary["data_structures"] = self.patterns["data_structures"]

        if self.patterns["function_calls"]["recursive"]:
            summary["recursion"] = self.patterns["function_calls"]

        return summary

    def get_all_patterns(self) -> Dict[str, Any]:
        """Get all detected patterns."""
        return self.patterns
