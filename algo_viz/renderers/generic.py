# algo_viz/renderers/generic.py
"""
Generic renderers for displaying behavior and pattern information.
User-friendly formatting with clear sections and helpful output.
"""

from typing import Dict, Any, List


def _section_header(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def render_behavior_summary(events) -> None:
    """Render a summary of function behavior."""
    from algo_viz.analyzers.behavior import BehaviorAnalyzer

    analyzer = BehaviorAnalyzer(events)
    _section_header("FUNCTION BEHAVIOR")

    # Input/Output
    io = analyzer.get_input_output()
    if io["inputs"]:
        print("\n[INPUT] Arguments:")
        for key, val in io["inputs"].items():
            val_repr = str(val) if len(str(val)) <= 50 else str(val)[:47] + "..."
            print(f"   • {key}: {val_repr} ({type(val).__name__})")

    if io["output_type"]:
        print(f"\n[OUTPUT] Type: {io['output_type']}")

    # Control Flow
    flow = analyzer.control_flow
    if flow["call_count"] > 0:
        print(f"\n[EXECUTION]")
        print(f"   • Function calls: {flow['call_count']}")
        print(f"   • Call depth: {flow['max_call_depth']}")

    # Complexity
    complexity = analyzer.get_complexity_indicators()
    if complexity["recursion_depth"] > 1:
        print(f"   • Recursion depth: {complexity['recursion_depth']}")
    if complexity["data_size"] > 0:
        print(f"   • Max data size: {complexity['data_size']} items")


def render_execution_stats(events) -> None:
    """Render execution statistics."""
    stats = {
        "total_events": len(events),
        "var_changes": 0,
        "calls": 0,
        "returns": 0,
        "unique_vars": set(),
    }

    for e in events:
        if e.event_type == "var_change":
            stats["var_changes"] += 1
            stats["unique_vars"].add(e.var_name)
        elif e.event_type == "call":
            stats["calls"] += 1
        elif e.event_type == "return":
            stats["returns"] += 1

    _section_header("EXECUTION STATISTICS")
    print(f"\n[TRACE SUMMARY]")
    print(f"   • Total events: {stats['total_events']}")
    print(f"   • Variable changes: {stats['var_changes']}")
    print(f"   • Unique variables: {len(stats['unique_vars'])}")
    print(f"   • Function calls: {stats['calls']}")
    print(f"   • Returns: {stats['returns']}")


def render_variable_tracking(events) -> None:
    """Render variable state changes with detailed transformations."""
    from algo_viz.analyzers.behavior import BehaviorAnalyzer
    from collections import defaultdict

    analyzer = BehaviorAnalyzer(events)
    var_flow = analyzer.get_variable_flow()

    if not var_flow["variables"]:
        return

    _section_header("VARIABLE TRACKING")

    # Categorize variables by activity level
    high_change_vars = []
    low_change_vars = []
    
    for var in var_flow["variables"]:
        if var['changes'] > 3:
            high_change_vars.append(var)
        else:
            low_change_vars.append(var)
    
    # Show high-activity variables first
    if high_change_vars:
        print("\n[HIGH ACTIVITY] (frequently changed):")
        for var in sorted(high_change_vars, key=lambda x: x['changes'], reverse=True):
            _print_variable_detail(var, events)
    
    # Show low-activity variables if any
    if low_change_vars:
        print("\n[LOW ACTIVITY] (set once or twice):")
        for var in sorted(low_change_vars, key=lambda x: x['changes']):
            _print_variable_detail(var, events)


def _print_variable_detail(var: Dict[str, Any], events) -> None:
    """Print detailed information about a single variable."""
    final_val = var['final_value']
    final_repr = str(final_val) if len(str(final_val)) <= 40 else str(final_val)[:37] + "..."
    
    # Collect value sequence for this variable
    value_sequence = []
    for e in events:
        if e.event_type == "var_change" and e.var_name == var['name']:
            if not value_sequence or value_sequence[-1] != e.new_value:
                value_sequence.append(e.new_value)
    
    # Print variable info
    print(f"\n   [{var['name']}]")
    print(f"      * State changes: {var['changes']}")
    
    # Show value transformation
    if value_sequence and len(value_sequence) > 1:
        # Show first and last value
        first_val = value_sequence[0]
        last_val = value_sequence[-1]
        first_repr = str(first_val)[:20]
        last_repr = str(last_val)[:20]
        print(f"      * Transforms from {first_repr} to {last_repr}")
        distinct_values = len(set(str(v) for v in value_sequence))
        if distinct_values <= 5:
            print(f"      * Takes {distinct_values} distinct value(s)")
    else:
        print(f"      * Final value: {final_repr}")
    
    # Show type conversions if any
    if var.get("type_changes", 0) > 0:
        print(f"      * Type conversions: {var['type_changes']}")


def render_pattern_summary(patterns: Dict[str, Any]) -> None:
    """Render detected patterns in a readable format."""
    if not patterns:
        return

    _section_header("DETECTED PATTERNS")

    for pattern_name, pattern_data in patterns.items():
        if isinstance(pattern_data, dict) and pattern_data.get("detected"):
            # Format pattern name
            display_name = pattern_name.replace('_', ' ').title()
            
            # Get count if available
            count_info = ""
            if "iteration_count" in pattern_data and pattern_data["iteration_count"]:
                count_info = f" ({pattern_data['iteration_count']}x)"
            elif "branches" in pattern_data and pattern_data["branches"]:
                count_info = f" ({pattern_data['branches']} branches)"
            
            print(f"\n[+] {display_name}{count_info}")
            
            # Show relevant details
            for key, val in pattern_data.items():
                if key not in ["detected"] and val:
                    if isinstance(val, (list, set)):
                        if val:
                            val_str = ", ".join(str(v) for v in val)
                            print(f"    • {key.replace('_', ' ')}: {val_str}")
                    elif isinstance(val, int):
                        print(f"    • {key.replace('_', ' ')}: {val}")


def render_operation_summary(operations: Dict[str, Any]) -> None:
    """Render summary of operations performed."""
    has_content = False

    # Check if there's anything to show
    loops = operations.get("loops", {})
    for_loop = loops.get("for") if isinstance(loops, dict) else False
    while_loop = loops.get("while") if isinstance(loops, dict) else False
    conditionals = operations.get("conditionals", {})
    
    if not (for_loop or while_loop or conditionals.get("detected") or 
            operations.get("data_structures", {}).get("detected_types") or
            operations.get("arithmetic", {}).get("detected")):
        return

    _section_header("OPERATIONS PERFORMED")

    # Loops
    if for_loop or while_loop:
        print("\n[LOOPS]")
        if for_loop:
            print(f"   > For loop detected")
        if while_loop:
            print(f"   > While loop detected")
        has_content = True

    # Conditionals
    if conditionals.get("detected"):
        print(f"\n[CONDITIONALS]")
        branches = conditionals.get("branches", 0)
        print(f"   • Branches: {branches}")
        if conditionals.get("early_returns"):
            print(f"   • Early returns: {conditionals['early_returns']}")
        has_content = True

    # Data Structures
    ds = operations.get("data_structures", {})
    if ds.get("detected_types"):
        print(f"\n[DATA STRUCTURES]")
        types_str = ", ".join(ds["detected_types"])
        print(f"   • Used: {types_str}")
        if ds.get("list_operations") > 0:
            print(f"   • List ops: {ds['list_operations']}")
        has_content = True

    # Arithmetic
    arith = operations.get("arithmetic", {})
    if arith.get("detected"):
        print(f"\n[ARITHMETIC]")
        print(f"   • Operations: {arith.get('numeric_ops', 0)}")
        if arith.get("increment_ops", 0) > 0:
            print(f"   • Increments: {arith['increment_ops']}")
        if arith.get("decrement_ops", 0) > 0:
            print(f"   • Decrements: {arith['decrement_ops']}")
        has_content = True


def render_data_flow(events) -> None:
    """Render data flow diagram (simplified)."""
    from collections import defaultdict

    var_origins = {}
    var_destinations = defaultdict(set)

    for e in events:
        if e.event_type == "var_change":
            if e.var_name not in var_origins:
                var_origins[e.var_name] = e.old_value
            var_destinations[e.var_name].add(e.new_value)

    if not var_origins:
        return

    _section_header("DATA FLOW")

    for var, origin in var_origins.items():
        destinations = var_destinations.get(var, set())
        if destinations and len(destinations) > 1:
            origin_repr = str(origin)[:30]
            print(f"\n  {var}:")
            print(f"     • Starts as: {origin_repr} ({type(origin).__name__})")
            print(f"     • Transforms to: {len(destinations)} different value(s)")



def render_pattern_summary(patterns: Dict[str, Any]) -> None:
    """Render detected patterns in a readable format."""
    if not patterns:
        print("\n[*] No significant patterns detected.")
        return

    print("\n[*] Detected Patterns:")
    print("------" * 10)

    for pattern_name, pattern_data in patterns.items():
        if isinstance(pattern_data, dict):
            if pattern_data.get("detected"):
                print(f"\n{pattern_name.replace('_', ' ').title()}:")
                for key, val in pattern_data.items():
                    if key != "detected" and val:
                        if isinstance(val, (list, set)):
                            val = ", ".join(str(v) for v in val)
                        print(f"  {key.replace('_', ' ')}: {val}")


def render_operation_summary(operations: Dict[str, Any]) -> None:
    """Render summary of operations performed."""
    print("\n[*] Operations Summary")
    print("------" * 10)

    if operations.get("loops", {}).get("detected"):
        loops = operations["loops"]
        print(f"\nLoops: {len(loops.get('loop_vars', []))} loop variable(s)")
        print(f"  Variables: {', '.join(loops.get('loop_vars', []))}")
        if loops.get("iteration_count"):
            print(f"  Iterations: ~{loops['iteration_count']}")

    if operations.get("conditionals", {}).get("detected"):
        cond = operations["conditionals"]
        print(f"\nConditionals: {cond.get('branches', 0)} branch(es)")
        if cond.get("early_returns"):
            print(f"  Early returns: {cond['early_returns']}")

    if operations.get("data_structures", {}).get("detected_types"):
        ds = operations["data_structures"]
        print(f"\nData Structures used: {', '.join(ds['detected_types'])}")
        if ds["list_operations"] > 0:
            print(f"  List operations: {ds['list_operations']}")

    if operations.get("arithmetic", {}).get("detected"):
        arith = operations["arithmetic"]
        print(f"\nArithmetic Operations: {arith['numeric_ops']}")
        if arith["increment_ops"] > 0:
            print(f"  Increments: {arith['increment_ops']}")
        if arith["decrement_ops"] > 0:
            print(f"  Decrements: {arith['decrement_ops']}")


def render_data_flow(events) -> None:
    """Render data flow diagram (simplified)."""
    from collections import defaultdict

    var_origins = {}
    var_destinations = defaultdict(set)

    for e in events:
        if e.event_type == "var_change":
            if e.var_name not in var_origins:
                var_origins[e.var_name] = e.old_value

            var_destinations[e.var_name].add(e.new_value)

    if not var_origins:
        return

    print("\n[*] Data Flow")
    print("------" * 10)

    for var, origin in var_origins.items():
        destinations = var_destinations.get(var, set())
        if destinations:
            print(f"\n{var}:")
            print(f"  From: {origin} ({type(origin).__name__})")
            print(f"  To: {len(destinations)} different value(s)")


def render_execution_stats(events) -> None:
    """Render execution statistics."""
    stats = {
        "total_events": len(events),
        "var_changes": 0,
        "calls": 0,
        "returns": 0,
        "unique_vars": set(),
    }

    for e in events:
        if e.event_type == "var_change":
            stats["var_changes"] += 1
            stats["unique_vars"].add(e.var_name)
        elif e.event_type == "call":
            stats["calls"] += 1
        elif e.event_type == "return":
            stats["returns"] += 1

    print("\n[*] Execution Statistics")
    print("------" * 10)
    print(f"\nTotal events: {stats['total_events']}")
    print(f"Variable changes: {stats['var_changes']}")
    print(f"Unique variables: {len(stats['unique_vars'])}")
    print(f"Function calls: {stats['calls']}")
    print(f"Returns: {stats['returns']}")
