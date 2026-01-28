# algo_viz/renderers/sliding_window.py

def render_sliding_window(events):
    """Visualize sliding window algorithm"""
    print("\n[*] Sliding Window Visualization")
    print("-" * 70)
    
    # Extract window positions and array data
    window_states = []
    array_values = {}
    array_name = None
    
    # Find pointers that control the window (typically left/right or start/end)
    window_pointers = []
    for e in events:
        if e.event_type == "var_change" and isinstance(e.new_value, int):
            if e.var_name in ['left', 'right', 'start', 'end', 'l', 'r']:
                if e.var_name not in window_pointers:
                    window_pointers.append(e.var_name)
    
    # Track window movements
    window_positions = {ptr: [] for ptr in window_pointers}
    
    for e in events:
        if e.event_type == "var_change":
            # Track array
            if "[" in (e.var_name or ""):
                parts = e.var_name.split("[")
                array_name = parts[0]
                if isinstance(e.new_value, list):
                    array_values[array_name] = e.new_value
            # Track window pointers
            elif e.var_name in window_pointers:
                window_positions[e.var_name].append((e.line_no, e.new_value))
    
    # Get the array
    array_data = array_values.get(array_name)
    if not array_data:
        return
    
    print(f"\nArray: {array_data}")
    print()
    
    # Create timeline visualization
    max_moves = max(len(moves) for moves in window_positions.values()) if window_positions else 0
    
    for step in range(max_moves):
        # Get current positions
        positions = {}
        for ptr, moves in window_positions.items():
            if step < len(moves):
                positions[ptr] = moves[step][1]
        
        if not positions:
            continue
        
        # Get window bounds
        left = positions.get('left', positions.get('l', 0))
        right = positions.get('right', positions.get('r', len(array_data) - 1))
        start = positions.get('start', left)
        end = positions.get('end', right)
        
        # Ensure valid range for visualization
        window_start = min(left, start, 0)
        window_end = max(right, end, len(array_data) - 1)
        
        # Draw window
        print(f"Step {step + 1}: ", end="")
        for idx in range(len(array_data)):
            if window_start <= idx <= window_end:
                if (left <= idx <= right) or (start <= idx <= end):
                    # Inside window
                    print(f"[{array_data[idx]}]", end="")
                else:
                    print(f" {array_data[idx]} ", end="")
            else:
                print(f" {array_data[idx]} ", end="")
        print()
        
        # Show pointer labels
        print(" " * 7 + "  ", end="")
        for idx in range(len(array_data)):
            labels = []
            if window_pointers:
                for ptr in window_pointers:
                    if ptr in positions and positions[ptr] == idx:
                        labels.append(ptr[0].upper())
            if labels:
                print(" " + "".join(labels) + " ", end="")
            else:
                print("   ", end="")
        print()
        print()
