# algo_viz/detectors/sliding_window.py

def detect_sliding_window(events):
    moves = {}

    for e in events:
        if (
            e.event_type == "var_change"
            and isinstance(e.old_value, int)
            and isinstance(e.new_value, int)
        ):
            delta = e.new_value - e.old_value
            if abs(delta) == 1:
                moves.setdefault(e.var_name, []).append(delta)

    if len(moves) < 2:
        return False

    expanding = any(all(d > 0 for d in deltas) for deltas in moves.values())
    shrinking = any(any(d < 0 for d in deltas) for deltas in moves.values())

    return expanding and shrinking
