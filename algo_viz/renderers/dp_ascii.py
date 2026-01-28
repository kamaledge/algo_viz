def render_dp(dp_events):
    print("\n[*] DP Table Evolution")
    print("-" * 60)

    for i, e in enumerate(dp_events, 1):
        if e.inputs:
            # Show formula with computed values
            formula_parts = []
            for idx_expr, value in e.inputs.items():
                formula_parts.append(f"{e.table}[{idx_expr}]={value}")
            formula = " + ".join(formula_parts)
            print(
                f"Step {i:02d} | Line {e.line_no} | "
                f"{e.table}[{e.index}] = {formula} -> {e.result}"
            )
        else:
            print(
                f"Step {i:02d} | Line {e.line_no} | "
                f"{e.table}[{e.index}] = {e.result}"
            )

