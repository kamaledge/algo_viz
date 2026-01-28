# algo_viz/detectors/recursion.py

def detect_recursion(events):
    call_depth = 0
    max_depth = 0

    for e in events:
        if e.event_type == "call":
            call_depth += 1
            max_depth = max(max_depth, call_depth)
        elif e.event_type == "return":
            call_depth -= 1

    return max_depth > 1
