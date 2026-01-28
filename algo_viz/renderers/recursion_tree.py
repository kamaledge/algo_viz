# algo_viz/renderers/recursion_tree.py

def render_recursion_tree(events):
    print("\n[*] Recursion Tree")
    print("-" * 40)
    
    has_recursion = False
    for e in events:
        if e.depth and e.depth > 1:
            has_recursion = True
            break
    
    if not has_recursion:
        return

    for e in events:
        if e.depth is None:
            continue
        indent = "  " * max(0, e.depth - 1)

        if e.event_type == "call":
            args = ", ".join(f"{k}={v}" for k, v in e.new_value.items())
            print(f"{indent}[+] {e.func_name}({args})")

        elif e.event_type == "return":
            print(f"{indent}[-] return {e.new_value}")
