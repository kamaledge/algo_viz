# algo_viz/renderers/ascii.py

def render(events):
    print("\n[*] Algorithm Trace")
    print("-" * 40)

    for i, e in enumerate(events, 1):
        if e.event_type == "var_change":
            print(
                f"Step {i:02d} | line {e.line_no} | "
                f"{e.var_name}: {e.old_value} -> {e.new_value}"
            )
