# algo_viz/detectors/pointers.py

def detect_two_pointers(events):
    pointer_moves = {}

    for e in events:
        if e.event_type == "var_change" and isinstance(e.old_value, int):
            delta = e.new_value - e.old_value
            if abs(delta) == 1:
                pointer_moves.setdefault(e.var_name, []).append(delta)

    pointers = [
        var for var, moves in pointer_moves.items()
        if all(d > 0 for d in moves) or all(d < 0 for d in moves)
    ]

    return len(pointers) >= 2
