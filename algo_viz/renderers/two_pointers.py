# algo_viz/renderers/two_pointers.py

def render_two_pointers(events):
    """Visualize two-pointer algorithm with array state"""
    print("\n[*] Two Pointers Visualization")
    print("-" * 70)
    
    # Extract array from function call arguments
    array_data = None
    for e in events:
        if e.event_type == "call" and isinstance(e.new_value, dict):
            # Look for list in arguments
            for key, val in e.new_value.items():
                if isinstance(val, list):
                    array_data = val
                    break
        if array_data:
            break
    
    if not array_data:
        return
    
    # Extract pointer movements
    pointer_moves = {}
    
    for e in events:
        if e.event_type == "var_change" and isinstance(e.new_value, int):
            var_name = e.var_name
            # Detect pointer variables
            if var_name in ['l', 'r', 'left', 'right', 'start', 'end', 'i', 'j', 'low', 'high']:
                if var_name not in pointer_moves:
                    pointer_moves[var_name] = []
                pointer_moves[var_name].append((e.line_no, e.new_value))
    
    if not pointer_moves:
        return
    
    print(f"\nArray: {array_data}\n")
    
    # Create timeline visualization
    max_moves = max(len(moves) for moves in pointer_moves.values()) if pointer_moves else 0
    
    for step in range(max_moves):
        # Get current positions for all pointers
        positions = {}
        for ptr, moves in pointer_moves.items():
            if step < len(moves):
                positions[ptr] = moves[step][1]
            elif moves:  # Use last known position if no more moves
                positions[ptr] = moves[-1][1]
        
        if not positions:
            continue
        
        # Draw array with pointers highlighted
        print(f"Step {step + 1}: ", end="")
        for idx, val in enumerate(array_data):
            # Find pointers at this position
            ptrs = [p for p, pos in positions.items() if pos == idx]
            
            if ptrs:
                # Highlight position with pointers
                ptr_labels = "(" + ",".join(sorted(ptrs)) + ")"
                print(f"[{val}]{ptr_labels} ", end="")
            else:
                print(f"[{val}] ", end="")
        
        print()
        
        # Show pointer values below
        for ptr in sorted(positions.keys()):
            print(f"  {ptr}={positions[ptr]}", end=" ")
        print("\n")

