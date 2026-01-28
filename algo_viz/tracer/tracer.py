# algo_viz/tracer/tracer.py

import sys
import dis
from .events import Event

class ExecutionTracer:
    def __init__(self):
        self.events = []
        self._prev_locals = {}
        self._depth = 0
        self._prev_list_states = {}
        self._list_access_log = []  # Track list[index] accesses

    def _get_list_changes(self, frame):
        """Detect which list indices changed by comparing list contents"""
        changes = []
        locals_now = frame.f_locals.copy()
        
        for var_name, val in locals_now.items():
            if isinstance(val, list) and not var_name.startswith("__"):
                prev_list = self._prev_list_states.get(var_name)
                if prev_list is not None:
                    # Handle lists of different lengths (expansion/contraction)
                    min_len = min(len(prev_list), len(val))
                    for i in range(min_len):
                        if prev_list[i] != val[i]:
                            changes.append((var_name, i, prev_list[i], val[i]))
                # Update state - copy to avoid mutation tracking issues
                try:
                    self._prev_list_states[var_name] = val.copy()
                except (TypeError, AttributeError):
                    # If list contains unmutable items, just reference it
                    self._prev_list_states[var_name] = list(val)
        
        return changes

    def _extract_formula_from_bytecode(self, frame):
        """Extract which list indices are being read from bytecode"""
        try:
            code = frame.f_code
            instructions = list(dis.get_instructions(code))
            
            # Find the current instruction
            offset = frame.f_lasti
            current_idx = None
            for i, instr in enumerate(instructions):
                if instr.offset <= offset < (instructions[i+1].offset if i+1 < len(instructions) else float('inf')):
                    current_idx = i
                    break
            
            if current_idx is None:
                return {}
            
            # Look backwards for BINARY_SUBSCR operations (list reads)
            reads = {}
            for i in range(max(0, current_idx - 20), current_idx + 1):
                instr = instructions[i]
                if instr.opname == 'BINARY_SUBSCR':
                    # This reads a list at an index
                    # We need to look at the stack state, but that's complex
                    # For now, return empty to avoid errors
                    pass
            
            return reads
        except Exception:
            return {}

    def _trace(self, frame, event, arg):
        func_name = frame.f_code.co_name

        if event == "call":
            self._depth += 1
            args = {
                k: v
                for k, v in frame.f_locals.items()
                if not k.startswith("__")
            }

            self.events.append(
                Event(
                    event_type="call",
                    line_no=frame.f_lineno,
                    func_name=func_name,
                    var_name=None,
                    old_value=None,
                    new_value=args,
                    depth=self._depth,
                )
            )
            return self._trace

        if event == "return":
            self.events.append(
                Event(
                    event_type="return",
                    line_no=frame.f_lineno,
                    func_name=func_name,
                    var_name=None,
                    old_value=None,
                    new_value=arg,
                    depth=self._depth,
                )
            )
            self._depth -= 1
            return self._trace

        if event == "line":
            locals_now = frame.f_locals.copy()
            
            # Track scalar variable changes
            for var, val in locals_now.items():
                if var in self._prev_locals and self._prev_locals[var] != val:
                    if not isinstance(val, (list, dict)):
                        self.events.append(
                            Event(
                                event_type="var_change",
                                line_no=frame.f_lineno,
                                func_name=func_name,
                                var_name=var,
                                old_value=self._prev_locals[var],
                                new_value=val,
                                depth=self._depth,
                            )
                        )
            
            # Track list index changes
            list_changes = self._get_list_changes(frame)
            for var_name, idx, old_v, new_v in list_changes:
                # Store the locals snapshot and source line for formula analysis
                try:
                    import linecache
                    # Get current and next lines to find the actual assignment
                    current_line = linecache.getline(frame.f_code.co_filename, frame.f_lineno).strip()
                    next_line = linecache.getline(frame.f_code.co_filename, frame.f_lineno + 1).strip()
                    
                    # If current line is a for/while loop, use the next line (the body)
                    if current_line.startswith('for ') or current_line.startswith('while '):
                        source_line = next_line
                    else:
                        source_line = current_line
                except Exception:
                    source_line = ""
                
                change_event = Event(
                    event_type="var_change",
                    line_no=frame.f_lineno,
                    func_name=func_name,
                    var_name=f"{var_name}[{idx}]",
                    old_value=old_v,
                    new_value=new_v,
                    depth=self._depth,
                )
                # Attach locals snapshot and source for formula analysis
                change_event.locals_snapshot = locals_now.copy()
                change_event.source_line = source_line
                change_event.filename = frame.f_code.co_filename
                self.events.append(change_event)
            
            self._prev_locals = locals_now

        return self._trace

    def run(self, func, *args, **kwargs):
        sys.settrace(self._trace)
        try:
            result = func(*args, **kwargs)
        finally:
            sys.settrace(None)
        return result, self.events
