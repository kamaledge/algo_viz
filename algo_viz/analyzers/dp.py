
from .events import DPUpdateEvent
import re

def is_list_assignment(e):
    return (
        e.event_type == "var_change"
        and (isinstance(e.new_value, int) or isinstance(e.new_value, list))
        and "[" in (e.var_name or "")
    )

def parse_var_name(var_name):
    """Extract table name and index from var_name like 'dp[i]' or 'memo[0][1]'"""
    match = re.match(r'(\w+)\[(.+)\]', var_name)
    if match:
        return match.group(1), match.group(2)
    return None, None

def extract_formula_from_source(source_line, locals_snapshot, table_name, result_value):
    """
    Extract formula from source line like 'dp[i] = dp[i-1] + dp[i-2]'
    Returns dict of {index_expr: value} pairs used in the computation
    """
    inputs = {}
    
    try:
        if not source_line or "=" not in source_line:
            return inputs
        
        # Get the RHS (right-hand side) of the assignment
        rhs = source_line.split("=", 1)[-1].strip()
        
        # Match all patterns like table[expr] in the RHS
        pattern = re.compile(rf'{re.escape(table_name)}\[([^\]]+)\]')
        matches = list(pattern.finditer(rhs))
        
        for match in matches:
            idx_expr = match.group(1)
            try:
                # Safely evaluate the index expression
                idx_value = eval(idx_expr, {"__builtins__": {}}, locals_snapshot)
                if isinstance(idx_value, int):
                    # Get the actual table value
                    table = locals_snapshot.get(table_name)
                    if isinstance(table, list) and 0 <= idx_value < len(table):
                        # Use the expression as key to preserve readability (e.g., "i-1")
                        inputs[idx_expr] = table[idx_value]
            except Exception:
                pass
        
        return inputs
    except Exception:
        return {}

def analyze_dp(events):
    dp_events = []

    for e in events:
        if is_list_assignment(e):
            table_name, index_expr = parse_var_name(e.var_name)
            if table_name and index_expr:
                inputs = {}
                
                # Try to extract formula from source code
                try:
                    locals_snapshot = getattr(e, 'locals_snapshot', {})
                    source_line = getattr(e, 'source_line', '')
                    
                    # Debug output
                    # print(f"DEBUG: source_line='{source_line}', table='{table_name}', has locals: {bool(locals_snapshot)}")
                    
                    if source_line and locals_snapshot:
                        inputs = extract_formula_from_source(
                            source_line,
                            locals_snapshot,
                            table_name,
                            e.new_value
                        )
                except Exception as ex:
                    # print(f"DEBUG: Exception in analyze_dp: {ex}")
                    pass
                
                dp_events.append(
                    DPUpdateEvent(
                        table=table_name,
                        index=index_expr,
                        inputs=inputs,
                        result=e.new_value,
                        line_no=e.line_no,
                    )
                )
    return dp_events
