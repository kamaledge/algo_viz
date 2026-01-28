# algo_viz/detectors/dp.py

def detect_dp(events):
    writes = {}

    for e in events:
        if (
            e.event_type == "var_change"
            and isinstance(e.old_value, (int, float))
            and isinstance(e.new_value, (int, float))
        ):
            # Skip list index changes - they should be detected separately
            if "[" in (e.var_name or ""):
                continue
            name = e.var_name
            writes.setdefault(name, 0)
            writes[name] += 1

    # Also detect if there are many list index assignments
    list_writes = {}
    for e in events:
        if (
            e.event_type == "var_change"
            and "[" in (e.var_name or "")
            and isinstance(e.new_value, (int, float))
        ):
            var_name = e.var_name.split("[")[0]
            list_writes.setdefault(var_name, 0)
            list_writes[var_name] += 1

    # heuristic: many numeric overwrites OR many list assignments → DP-like
    return any(count >= 3 for count in writes.values()) or any(count >= 3 for count in list_writes.values())
