# algo_viz/renderers/ascii.py

def render(events):
    print("\n[*] Algorithm Trace")
    print("-" * 40)

    # Collect all variable names
    var_names = set()
    for e in events:
        if e.event_type == "var_change":
            var_names.add(e.var_name)

    # Maintain current values
    current_values = {}

    for i, e in enumerate(events, 1):
        if e.event_type == "var_change":
            current_values[e.var_name] = e.new_value
            # Print the change
            var_list = ", ".join(f"{name}={current_values.get(name, 'undefined')}" for name in sorted(var_names))
            print(
                f"Step {i:02d} | line {e.line_no} | "
                f"{e.var_name}: {e.old_value} -> {e.new_value} | Variables: {var_list}"
            )
