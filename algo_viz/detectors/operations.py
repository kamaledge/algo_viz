# algo_viz/detectors/operations.py
"""
Detectors for specific operations like loops, conditionals, and data structure manipulations.
"""

from typing import List, Dict, Set, Any
from collections import defaultdict


def detect_for_loops(events) -> bool:
    """Detect for loop patterns through repeated variable increments."""
    increment_sequences = defaultdict(list)

    for e in events:
        if (
            e.event_type == "var_change"
            and isinstance(e.old_value, int)
            and isinstance(e.new_value, int)
        ):
            if e.new_value - e.old_value == 1:
                increment_sequences[e.var_name].append(e)

    # If any variable increments by 1 multiple times, it's likely a loop counter
    return any(len(seq) >= 2 for seq in increment_sequences.values())


def detect_while_loops(events) -> bool:
    """Detect while loop patterns through repeated conditional changes."""
    # While loops typically have repeated condition evaluations
    # This is detected through repeated variable changes without clear loop variable
    var_change_counts = defaultdict(int)

    for e in events:
        if e.event_type == "var_change":
            var_change_counts[e.var_name] += 1

    # Multiple variables changing repeatedly suggests while loop
    multi_var_changes = sum(1 for count in var_change_counts.values() if count > 2)
    return multi_var_changes >= 2


def detect_nested_loops(events) -> Dict[str, Any]:
    """Detect nested loop patterns."""
    nested_info = {
        "detected": False,
        "nesting_level": 0,
        "loop_variables": [],
    }

    # Track variable modification patterns at different depths
    depth_vars = defaultdict(set)

    for e in events:
        if e.event_type == "var_change":
            depth_vars[e.depth].add(e.var_name)

    # Multiple depths with active variables suggest nesting
    active_depths = len([d for d in depth_vars if len(depth_vars[d]) > 0])

    if active_depths > 1:
        nested_info["detected"] = True
        nested_info["nesting_level"] = active_depths

    return nested_info


def detect_if_else(events) -> Dict[str, Any]:
    """Detect if/else conditional patterns."""
    if_else_info = {
        "detected": False,
        "branches": 0,
        "has_else": False,
    }

    # Look for early returns or variable divergence
    max_depth = 0
    for e in events:
        if e.event_type == "call":
            max_depth = max(max_depth, e.depth or 0)

    # Count returns at different depths
    return_depths = defaultdict(int)
    for e in events:
        if e.event_type == "return":
            return_depths[e.depth or 0] += 1

    if len(return_depths) > 1:
        if_else_info["detected"] = True
        if_else_info["branches"] = len(return_depths)
        if_else_info["has_else"] = True

    return if_else_info


def detect_list_operations(events) -> Dict[str, Any]:
    """Detect list manipulation operations."""
    list_ops = {
        "read_count": 0,
        "write_count": 0,
        "accessed_lists": set(),
        "operations": [],
    }

    for e in events:
        if e.event_type == "var_change":
            if "[" in (e.var_name or "") and "]" in (e.var_name or ""):
                list_name = e.var_name.split("[")[0]
                list_ops["accessed_lists"].add(list_name)

                # Distinguish reads vs writes based on value changes
                if e.old_value != e.new_value:
                    list_ops["write_count"] += 1
                    list_ops["operations"].append(("write", list_name))
                else:
                    list_ops["read_count"] += 1
                    list_ops["operations"].append(("read", list_name))

    list_ops["accessed_lists"] = list(list_ops["accessed_lists"])
    return list_ops


def detect_dict_operations(events) -> Dict[str, Any]:
    """Detect dictionary manipulation operations."""
    dict_ops = {
        "operations": 0,
        "keys_accessed": set(),
    }

    for e in events:
        if e.event_type == "var_change":
            if isinstance(e.new_value, dict) or isinstance(e.old_value, dict):
                dict_ops["operations"] += 1

    dict_ops["keys_accessed"] = list(dict_ops["keys_accessed"])
    return dict_ops


def detect_set_operations(events) -> Dict[str, Any]:
    """Detect set operations like add, remove, intersection, etc."""
    set_ops = {
        "operations": 0,
        "types": [],
    }

    for e in events:
        if e.event_type == "var_change":
            if isinstance(e.new_value, set):
                set_ops["operations"] += 1
                if "add" not in set_ops["types"]:
                    set_ops["types"].append("add/modify")

    return set_ops


def detect_string_operations(events) -> Dict[str, Any]:
    """Detect string manipulation operations."""
    string_ops = {
        "operations": 0,
        "transformations": 0,
    }

    for e in events:
        if e.event_type == "var_change":
            if isinstance(e.new_value, str):
                string_ops["operations"] += 1
                if isinstance(e.old_value, str) and e.old_value != e.new_value:
                    string_ops["transformations"] += 1

    return string_ops


def detect_accumulation(events) -> Dict[str, Any]:
    """Detect accumulation patterns (sum, product, etc.)."""
    accumulation = {
        "detected": False,
        "accumulator_vars": [],
        "operations_count": 0,
    }

    var_operations = defaultdict(list)

    for e in events:
        if (
            e.event_type == "var_change"
            and isinstance(e.old_value, (int, float))
            and isinstance(e.new_value, (int, float))
        ):
            var_operations[e.var_name].append((e.old_value, e.new_value))

    # Look for variables that grow or shrink monotonically
    for var, operations in var_operations.items():
        if len(operations) > 1:
            # Check if it's accumulating (always increasing or always decreasing)
            is_accumulating = True
            for i in range(1, len(operations)):
                if operations[i][1] <= operations[i - 1][1]:
                    is_accumulating = False
                    break

            if is_accumulating:
                accumulation["detected"] = True
                accumulation["accumulator_vars"].append(var)
                accumulation["operations_count"] += len(operations)

    return accumulation


def detect_search_pattern(events) -> Dict[str, Any]:
    """Detect search patterns (linear search, binary search)."""
    search = {
        "detected": False,
        "pattern_type": None,
        "iterations": 0,
    }

    # Look for patterns of comparisons followed by pointer movements
    comparisons = 0
    pointer_moves = 0

    for e in events:
        if e.event_type == "var_change":
            if isinstance(e.new_value, bool):
                comparisons += 1
            elif isinstance(e.old_value, int) and isinstance(e.new_value, int):
                if abs(e.new_value - e.old_value) <= 1:
                    pointer_moves += 1

    if comparisons > 0 and pointer_moves > 0:
        search["detected"] = True
        search["iterations"] = max(comparisons, pointer_moves)

    return search


def detect_sorting_pattern(events) -> Dict[str, Any]:
    """Detect sorting-like patterns through repeated swaps and comparisons."""
    sorting = {
        "detected": False,
        "swap_count": 0,
        "comparison_count": 0,
    }

    # Look for patterns of repeated element exchanges
    list_changes = defaultdict(int)

    for e in events:
        if e.event_type == "var_change" and "[" in (e.var_name or ""):
            list_changes[e.var_name] += 1

    # Many list index changes suggest sorting
    if any(count > 5 for count in list_changes.values()):
        sorting["detected"] = True
        sorting["swap_count"] = sum(list_changes.values()) // 2

    return sorting
