# AlgoViz Architecture: Complete End-to-End Flow

**This guide explains exactly how AlgoViz works from start to finish, with concrete examples you can trace through the code.**

---

## Table of Contents
1. [Quick Overview](#quick-overview)
2. [Complete Flow Diagram](#complete-flow-diagram)
3. [Step-by-Step Execution](#step-by-step-execution)
4. [Component Deep Dive](#component-deep-dive)
5. [Data Structures](#data-structures)
6. [Real Example Walkthrough](#real-example-walkthrough)
7. [Extension Points](#extension-points)

---

## Quick Overview

```
User writes function with @visualize() decorator
            ↓
Decorator intercepts function call
            ↓
ExecutionTracer hooks into Python runtime with sys.settrace()
            ↓
Function executes while tracer captures every detail
            ↓
Event list collected (var changes, calls, returns, etc.)
            ↓
Pattern detectors analyze events
            ↓
Behavior analyzer extracts insights
            ↓
Rendering functions format output
            ↓
Console displays visualization
```

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ USER CODE                                                   │
│ @visualize(show_generic=True, mode="ascii")                │
│ def find_max(arr):                                          │
│     max_val = arr[0]                                        │
│     for x in arr:                                           │
│         if x > max_val: max_val = x                         │
│     return max_val                                          │
│                                                             │
│ result = find_max([3, 7, 2, 9, 1])                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ DECORATORS.PY - @visualize()                                │
│ - Creates wrapper function                                  │
│ - Initializes ExecutionTracer                               │
│ - Calls function with tracer                                │
│ - Orchestrates analysis & rendering                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ TRACER - sys.settrace() Hook                                │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Python Runtime Events:                                  │ │
│ │  - Function call: find_max([3,7,2,9,1])               │ │
│ │  - Line execution: max_val = arr[0]                    │ │
│ │  - Variable change: max_val: undefined → 3            │ │
│ │  - Line execution: for x in arr:                       │ │
│ │  - Variable change: x: undefined → 3                  │ │
│ │  - Condition check: if x > max_val                    │ │
│ │  - ... (more events)                                   │ │
│ │  - Return: return 9                                    │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ EVENTS LIST                                                 │
│ [                                                           │
│   Event(type='call', func='find_max', args=([3,7,2,9,1],)),│
│   Event(type='var_change', var='max_val', old=None, new=3),│
│   Event(type='var_change', var='x', old=None, new=3),      │
│   Event(type='var_change', var='x', old=3, new=7),         │
│   Event(type='var_change', var='max_val', old=3, new=7),   │
│   ... more events ...                                       │
│   Event(type='return', value=9)                             │
│ ]                                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┬──────────────┐
         ▼             ▼             ▼              ▼
    ┌────────────┐ ┌──────────┐ ┌─────────────┐ ┌─────────────┐
    │ Detectors  │ │Analyzers │ │  Renderers  │ │  Pattern    │
    │            │ │          │ │             │ │  Detectors  │
    │- Recursion │ │-Behavior │ │- Behavior   │ │- Generic    │
    │- DP        │ │          │ │- Stats      │ │- Loops      │
    │- 2Ptr      │ │          │ │- Variables  │ │- Cond.      │
    │- SlidWin   │ │          │ │- Patterns   │ │- Data struct│
    │            │ │          │ │- Operations │ │             │
    └────────────┘ └──────────┘ └─────────────┘ └─────────────┘
         │             │             │              │
         └─────────────┼─────────────┼──────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ ANALYSIS RESULTS                                            │
│ {                                                           │
│   "detected_patterns": ["Two Pointers", "Loop"],           │
│   "input_args": {"arr": [3,7,2,9,1]},                      │
│   "output_type": "int",                                     │
│   "variables": [                                            │
│     {"name": "max_val", "changes": 4, ...},               │
│     {"name": "x", "changes": 5, ...}                       │
│   ],                                                        │
│   "operations": {"loops": {"for": True}, ...}              │
│ }                                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ RENDERING PIPELINE (decorators.py)                          │
│ 1. render_behavior_summary()       → Input/Output overview  │
│ 2. render_execution_stats()        → Event metrics          │
│ 3. render_pattern_summary()        → Detected patterns      │
│ 4. render_operation_summary()      → Operations found       │
│ 5. render_variable_tracking()      → Variable lifecycle     │
│ 6. render_data_flow()              → Value transformations  │
│ 7. render() [from ascii.py]        → Algorithm trace        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ CONSOLE OUTPUT                                              │
│                                                             │
│ ============================================================│
│   FUNCTION BEHAVIOR                                         │
│ ============================================================│
│                                                             │
│ [INPUT] Arguments:                                          │
│    * arr: [3, 7, 2, 9, 1] (list)                           │
│                                                             │
│ [OUTPUT] Type: int                                          │
│ ... (more output) ...                                       │
│                                                             │
│ [HIGH ACTIVITY] (frequently changed):                       │
│                                                             │
│    [max_val]                                                │
│       * State changes: 4                                    │
│       * Transforms from 3 to 9                              │
│       * Takes 4 distinct value(s)                           │
│                                                             │
│ ... (rest of output) ...                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Execution

### Phase 1: Decoration & Setup

**File: decorators.py (lines 30-50)**

```python
@visualize(show_generic=True, mode="ascii")
def find_max(arr):
    ...

# What happens:
# 1. @visualize is called with parameters
# 2. Returns a decorator function
# 3. Decorator wraps find_max function
# 4. Returns the wrapper (inner function)
```

**Decorator Code:**
```python
def visualize(mode="ascii", show_generic=False):
    def wrapper(func):
        def inner(*args, **kwargs):
            # This is what actually runs
            tracer = ExecutionTracer()  # ← Create tracer
            result = tracer.run(func, args, kwargs)  # ← Run function with tracing
            events = tracer.events  # ← Get captured events
            
            # Then analyze and render...
            return result
        return inner
    return wrapper
```

**Key Point**: The `inner` function is what runs when you call `find_max([3,7,2,9,1])`.

---

### Phase 2: Execution & Tracing

**File: tracer/tracer.py**

```python
class ExecutionTracer:
    def __init__(self):
        self.events = []  # ← Will store all events here
    
    def run(self, func, args, kwargs):
        # 1. Install trace hook
        sys.settrace(self.trace_function)
        
        # 2. Execute user function
        result = func(*args, **kwargs)  # ← User code runs HERE
        
        # 3. Remove trace hook
        sys.settrace(None)
        
        return result
```

**What happens during function execution:**

When you call `find_max([3,7,2,9,1])`, Python is being traced by `trace_function`:

```python
def trace_function(self, frame, event, arg):
    # Called for EVERY line execution, variable assignment, etc.
    
    if event == "call":
        # A function was called
        self.events.append(Event(
            event_type="call",
            func_name=frame.f_code.co_name,
            ...
        ))
    
    elif event == "return":
        # A function returned
        self.events.append(Event(
            event_type="return",
            return_value=arg,
            ...
        ))
    
    elif event == "line":
        # A line of code executed
        # Check for variable changes since last line
        current_locals = frame.f_locals
        for var_name in current_locals:
            if var_name not in self.previous_locals:
                # New variable
                self.events.append(Event(
                    event_type="var_change",
                    var_name=var_name,
                    old_value=None,
                    new_value=current_locals[var_name]
                ))
            elif current_locals[var_name] != self.previous_locals[var_name]:
                # Variable changed
                self.events.append(Event(
                    event_type="var_change",
                    var_name=var_name,
                    old_value=self.previous_locals[var_name],
                    new_value=current_locals[var_name]
                ))
        self.previous_locals = current_locals.copy()
    
    return self.trace_function
```

**Result**: After function executes, `self.events` contains something like:

```python
[
    Event(type='call', func='find_max', args=([3,7,2,9,1],)),
    Event(type='var_change', var='max_val', old=None, new=3),
    Event(type='var_change', var='x', old=None, new=3),
    Event(type='var_change', var='x', old=3, new=7),
    Event(type='var_change', var='max_val', old=3, new=7),
    Event(type='var_change', var='x', old=7, new=2),
    Event(type='var_change', var='x', old=2, new=9),
    Event(type='var_change', var='max_val', old=7, new=9),
    Event(type='var_change', var='x', old=9, new=1),
    Event(type='return', value=9),
]
```

---

### Phase 3: Pattern Detection

**File: decorators.py (lines 55-70)**

After execution, the decorator detects what algorithm pattern was used:

```python
# Check for specific algorithms
detected_patterns = []

if detect_two_pointers(events):
    detected_patterns.append("Two Pointers")

if detect_recursion(events):
    detected_patterns.append("Recursion")

if detect_dp(events):
    detected_patterns.append("Dynamic Programming")

if detect_sliding_window(events):
    detected_patterns.append("Sliding Window")

# Generic pattern detection (works on ANY function)
generic_detector = GenericPatternDetector()
generic_patterns = generic_detector.detect(events)
```

**Example: How `detect_recursion()` works:**

```python
def detect_recursion(events):
    """Check if function called itself"""
    for event in events:
        if event.event_type == "call":
            if event.func_name == events[0].func_name:  # Calling itself
                return True
    return False
```

**Generic Detection: How loops are found**

```python
# In detectors/generic.py
class GenericPatternDetector:
    def detect(self, events):
        patterns = {}
        
        # Look for loops by finding repeated variable patterns
        patterns['loops'] = self.detect_loops(events)
        patterns['conditionals'] = self.detect_conditionals(events)
        patterns['data_structures'] = self.detect_data_structures(events)
        
        return patterns
    
    def detect_loops(self, events):
        """Find loop patterns"""
        loop_vars = set()
        var_change_counts = {}
        
        for event in events:
            if event.event_type == "var_change":
                var = event.var_name
                var_change_counts[var] = var_change_counts.get(var, 0) + 1
                
                # If a variable changed multiple times, likely in a loop
                if var_change_counts[var] > 2:
                    loop_vars.add(var)
        
        return {
            "detected": len(loop_vars) > 0,
            "loop_vars": list(loop_vars),
            "iteration_count": max(var_change_counts.values()) if var_change_counts else 0
        }
```

---

### Phase 4: Behavior Analysis

**File: analyzers/behavior.py**

```python
class BehaviorAnalyzer:
    def __init__(self, events):
        self.events = events
    
    def get_input_output(self):
        """Extract input and output"""
        inputs = {}
        output_type = None
        
        # Find the call event (has input args)
        for event in self.events:
            if event.event_type == "call":
                inputs = event.args  # ← Arguments passed
        
        # Find the return event (has return value)
        for event in self.events:
            if event.event_type == "return":
                output_type = type(event.return_value).__name__
        
        return {"inputs": inputs, "output_type": output_type}
    
    def get_variable_flow(self):
        """Track how variables change"""
        variables = {}
        
        for event in self.events:
            if event.event_type == "var_change":
                var_name = event.var_name
                
                if var_name not in variables:
                    variables[var_name] = {
                        "name": var_name,
                        "changes": 0,
                        "type_changes": 0,
                        "initial_value": event.old_value,
                        "final_value": event.new_value
                    }
                
                variables[var_name]["changes"] += 1
                variables[var_name]["final_value"] = event.new_value
                
                # Track type changes
                if event.old_value is not None:
                    if type(event.old_value) != type(event.new_value):
                        variables[var_name]["type_changes"] += 1
        
        return {"variables": list(variables.values())}
```

**Result: Analysis Data**

```python
{
    "inputs": {"arr": [3, 7, 2, 9, 1]},
    "output_type": "int",
    "variables": [
        {
            "name": "max_val",
            "changes": 4,
            "type_changes": 0,
            "initial_value": 3,
            "final_value": 9
        },
        {
            "name": "x",
            "changes": 5,
            "type_changes": 0,
            "initial_value": 3,
            "final_value": 1
        }
    ]
}
```

---

### Phase 5: Rendering

**File: decorators.py (lines 85-105) & renderers/generic.py**

The decorator calls renderers in sequence:

```python
if show_generic:
    if mode == "ascii":
        # 1. High-level behavior
        render_behavior_summary(events)
        
        # 2. Execution metrics
        render_execution_stats(events)
        
        # 3. Detected patterns
        if generic_patterns:
            render_pattern_summary(generic_patterns)
        
        # 4. Operations performed
        if any(operations.values()):
            render_operation_summary(operations)
        
        # 5. Variable details
        render_variable_tracking(events)
        
        # 6. Data transformations
        render_data_flow(events)
        
        # 7. Algorithm trace
        render(events)
```

**Example: Variable Tracking Renderer**

```python
def render_variable_tracking(events) -> None:
    """Show how variables change during execution."""
    analyzer = BehaviorAnalyzer(events)
    var_flow = analyzer.get_variable_flow()
    
    if not var_flow["variables"]:
        return
    
    _section_header("VARIABLE TRACKING")
    
    # Categorize by activity
    high_change = [v for v in var_flow["variables"] if v['changes'] > 3]
    low_change = [v for v in var_flow["variables"] if v['changes'] <= 3]
    
    # Render high activity first
    if high_change:
        print("\n[HIGH ACTIVITY] (frequently changed):")
        for var in sorted(high_change, key=lambda x: x['changes'], reverse=True):
            _print_variable_detail(var, events)
    
    # Then low activity
    if low_change:
        print("\n[LOW ACTIVITY] (set once or twice):")
        for var in sorted(low_change, key=lambda x: x['changes']):
            _print_variable_detail(var, events)


def _print_variable_detail(var, events):
    """Print details about a single variable."""
    print(f"\n   [{var['name']}]")
    print(f"      * State changes: {var['changes']}")
    
    # Show transformation path
    value_sequence = []
    for e in events:
        if e.event_type == "var_change" and e.var_name == var['name']:
            if not value_sequence or value_sequence[-1] != e.new_value:
                value_sequence.append(e.new_value)
    
    if value_sequence and len(value_sequence) > 1:
        first = value_sequence[0]
        last = value_sequence[-1]
        print(f"      * Transforms from {first} to {last}")
        print(f"      * Takes {len(set(str(v) for v in value_sequence))} distinct value(s)")
    else:
        print(f"      * Final value: {var['final_value']}")
```

**Output:**

```
============================================================
  VARIABLE TRACKING
============================================================

[HIGH ACTIVITY] (frequently changed):

   [max_val]
      * State changes: 4
      * Transforms from 3 to 9
      * Takes 4 distinct value(s)

[LOW ACTIVITY] (set once or twice):

   [x]
      * State changes: 5
      * Transforms from 3 to 1
      * Takes 5 distinct value(s)
```

---

## Component Deep Dive

### 1. ExecutionTracer (tracer/tracer.py)

**Purpose**: Capture function execution details

**Key Methods**:

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| `run()` | function, args, kwargs | return value | Execute and trace function |
| `trace_function()` | frame, event, arg | trace_function | Called on every line/call/return |
| `get_events()` | - | list of Event | Get all captured events |

**How it works**:

```python
tracer = ExecutionTracer()

# 1. Install hook
sys.settrace(tracer.trace_function)

# 2. User function runs with tracing
result = find_max([3,7,2,9,1])

# 3. Hook removed
sys.settrace(None)

# 4. Access captured events
events = tracer.events  # ← All details of execution
```

---

### 2. Pattern Detectors (detectors/)

**Purpose**: Identify algorithm patterns

**Types**:

| Detector | Finds | Uses |
|----------|-------|------|
| `detect_recursion()` | Function calls itself | Recursion depth, call count |
| `detect_dp()` | Memoization pattern | Cache usage, state transitions |
| `detect_two_pointers()` | Pointer manipulation | Pointer moves, convergence |
| `detect_sliding_window()` | Window pattern | Window size, position changes |
| `GenericPatternDetector` | Any pattern | Loops, conditionals, data structs |

**Generic Detection Logic**:

```python
class GenericPatternDetector:
    def detect(self, events):
        # Count variable changes
        var_changes = {}
        for event in events:
            if event.event_type == "var_change":
                var_name = event.var_name
                var_changes[var_name] = var_changes.get(var_name, 0) + 1
        
        # Variables with high changes → likely in loops
        loop_vars = {v: c for v, c in var_changes.items() if c > 2}
        
        # Variables with low changes → likely parameters or simple assignments
        non_loop_vars = {v: c for v, c in var_changes.items() if c <= 2}
        
        return {
            "loops": {
                "detected": len(loop_vars) > 0,
                "variables": list(loop_vars.keys()),
                "iteration_count": max(loop_vars.values()) if loop_vars else 0
            }
        }
```

---

### 3. BehaviorAnalyzer (analyzers/behavior.py)

**Purpose**: Extract insights from execution

**Key Methods**:

```python
class BehaviorAnalyzer:
    def get_input_output(self):
        # Extract what was passed in and what was returned
        
    def get_variable_flow(self):
        # Track how each variable changes
        
    def get_complexity_indicators(self):
        # Estimate O(n) complexity
        
    def control_flow(self):
        # How many calls, returns, recursion depth
```

---

### 4. Renderers (renderers/)

**Purpose**: Format analysis into human-readable output

**Generic Renderers** (renderers/generic.py):

```python
render_behavior_summary()      # Function inputs/outputs
render_execution_stats()        # Trace metrics (events, changes, calls)
render_variable_tracking()      # Variable lifecycle & transformations
render_pattern_summary()        # Detected algorithm patterns
render_operation_summary()      # Operations (loops, conditionals, etc.)
render_data_flow()              # Variable value transformations
```

**Specialized Renderers** (for specific algorithms):

```python
render()                        # Generic algorithm trace
render_dp()                     # DP state table
render_two_pointers()           # Pointer positions
render_recursion_tree()         # Recursion call tree
```

---

## Data Structures

### Event Object

**Location**: `tracer/events.py`

```python
class Event:
    event_type: str          # "call", "return", "var_change", "line"
    timestamp: float         # When it happened
    
    # For var_change events:
    var_name: str           # Name of variable
    old_value: Any          # Previous value
    new_value: Any          # New value
    
    # For call/return events:
    func_name: str          # Name of function
    return_value: Any       # Value returned (for return events)
    args: tuple             # Arguments (for call events)
    
    # Source location:
    line_number: int        # Line in source file
    source_line: str        # Actual code line
```

### Analysis Result

**From BehaviorAnalyzer**:

```python
{
    "inputs": {
        "arr": [3, 7, 2, 9, 1]
    },
    "output_type": "int",
    "variables": [
        {
            "name": "max_val",
            "changes": 4,
            "type_changes": 0,
            "initial_value": 3,
            "final_value": 9
        }
    ],
    "control_flow": {
        "call_count": 1,
        "max_call_depth": 1,
        "recursion_depth": 1
    }
}
```

### Pattern Detection Result

**From GenericPatternDetector**:

```python
{
    "loops": {
        "detected": True,
        "iteration_count": 5,
        "loop_vars": ["x", "max_val"],
        "for": True,
        "while": False
    },
    "conditionals": {
        "detected": True,
        "branches": 2,
        "early_returns": 0
    },
    "data_structures": {
        "detected_types": ["list"],
        "list_operations": 3
    },
    "arithmetic": {
        "detected": True,
        "numeric_ops": 4,
        "increment_ops": 0,
        "comparison_ops": 5
    }
}
```

---

## Real Example Walkthrough

Let's trace `find_max([3, 7, 2, 9, 1])` completely:

### Step 1: Decorator Setup

```python
@visualize(show_generic=True, mode="ascii")
def find_max(arr):
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val

result = find_max([3, 7, 2, 9, 1])
```

The decorator wraps the function. When you call it, `inner()` executes.

### Step 2: Tracer Executes

```python
def inner(*args, **kwargs):  # args = ([3,7,2,9,1],)
    tracer = ExecutionTracer()
    
    # Set trace hook
    sys.settrace(tracer.trace_function)
    
    # Execute find_max with tracing active
    result = find_max([3, 7, 2, 9, 1])
    # ↓ User code runs with tracing ↓
    
    sys.settrace(None)  # Remove hook
```

### Step 3: Tracer Captures Events

During execution, `trace_function` is called repeatedly:

```
Event 1: call
  - func: find_max
  - args: ([3,7,2,9,1],)

Event 2: line (line 10: max_val = arr[0])
  - var_change: max_val: None → 3

Event 3: line (line 11: for x in arr:)
  - var_change: x: None → 3

Event 4: line (line 12: if x > max_val:)
  - False, skip body
  - var_change: x: 3 → 7

Event 5: line (line 12: if x > max_val:)
  - True, enter body
  - var_change: max_val: 3 → 7

Event 6: line
  - var_change: x: 7 → 2

Event 7: line (line 12: if x > max_val:)
  - False

Event 8: line
  - var_change: x: 2 → 9

Event 9: line (line 12: if x > max_val:)
  - True
  - var_change: max_val: 7 → 9

Event 10: line
  - var_change: x: 9 → 1

Event 11: line (line 12: if x > max_val:)
  - False

Event 12: return
  - return_value: 9
```

### Step 4: Pattern Detection

```python
# Detect recursion
detect_recursion(events) → False  # find_max doesn't call itself

# Detect DP
detect_dp(events) → False  # No memoization

# Detect two pointers
detect_two_pointers(events) → False  # No pointer manipulation

# Detect sliding window
detect_sliding_window(events) → False  # No window pattern

# Generic detection
generic_patterns = GenericPatternDetector().detect(events)
# ↓ Result:
{
    "loops": {
        "detected": True,
        "loop_vars": ["x", "max_val"],
        "iteration_count": 5
    },
    "conditionals": {
        "detected": True,
        "branches": 2
    },
    "data_structures": {
        "detected_types": ["list"],
        "list_operations": 1  # arr[0]
    },
    "arithmetic": {
        "detected": True,
        "numeric_ops": 5  # comparisons
    }
}
```

### Step 5: Behavior Analysis

```python
analyzer = BehaviorAnalyzer(events)

input_output = analyzer.get_input_output()
# ↓ Result:
{
    "inputs": {"arr": [3, 7, 2, 9, 1]},
    "output_type": "int"
}

var_flow = analyzer.get_variable_flow()
# ↓ Result:
{
    "variables": [
        {
            "name": "max_val",
            "changes": 4,
            "type_changes": 0,
            "initial_value": 3,
            "final_value": 9
        },
        {
            "name": "x",
            "changes": 5,
            "type_changes": 0,
            "initial_value": 3,
            "final_value": 1
        }
    ]
}

complexity = analyzer.get_complexity_indicators()
# ↓ Result:
{
    "recursion_depth": 1,
    "data_size": 5,
    "call_count": 1
}
```

### Step 6: Rendering

```python
# 1. Behavior Summary
render_behavior_summary(events)
# Output:
# ============================================================
#   FUNCTION BEHAVIOR
# ============================================================
# [INPUT] Arguments:
#    * arr: [3, 7, 2, 9, 1] (list)
# [OUTPUT] Type: int
# [EXECUTION]
#    * Function calls: 1
#    * Call depth: 1

# 2. Execution Stats
render_execution_stats(events)
# Output:
# ============================================================
#   EXECUTION STATISTICS
# ============================================================
# [TRACE SUMMARY]
#    * Total events: 12
#    * Variable changes: 9
#    * Unique variables: 2
#    * Function calls: 1
#    * Returns: 1

# 3. Pattern Summary
render_pattern_summary(generic_patterns)
# Output:
# ============================================================
#   DETECTED PATTERNS
# ============================================================
# [+] Loops (5x)
#     * loop vars: x, max_val
#     * iteration count: 5

# 4. Variable Tracking
render_variable_tracking(events)
# Output:
# ============================================================
#   VARIABLE TRACKING
# ============================================================
# [HIGH ACTIVITY] (frequently changed):
#    [max_val]
#       * State changes: 4
#       * Transforms from 3 to 9
#       * Takes 4 distinct value(s)
#    [x]
#       * State changes: 5
#       * Transforms from 3 to 1
#       * Takes 5 distinct value(s)

# ... more rendering ...
```

### Step 7: Return Value

```python
return result  # = 9
```

---

## Extension Points

### How to Add a New Detector

**Example: Detect if function modifies input array**

1. Create file: `detectors/mutation.py`

```python
def detect_array_mutation(events):
    """Detect if input array was modified"""
    for event in events:
        if event.event_type == "var_change":
            # Check if it's the array and it changed
            if event.var_name == "arr":
                if event.old_value != event.new_value:
                    return True
    return False
```

2. Register in `decorators.py`:

```python
from .detectors.mutation import detect_array_mutation

# In visualize wrapper:
if detect_array_mutation(events):
    detected_patterns.append("Array Mutation")
    print("[!] WARNING: Input array was modified!")
```

### How to Add a New Analyzer

**Example: Analyze function purity (does it modify inputs?)**

1. Add method to `BehaviorAnalyzer`:

```python
def is_pure(self):
    """Check if function is pure (doesn't modify inputs)"""
    mutations = 0
    for event in self.events:
        if event.event_type == "var_change":
            # Count parameter modifications
            if event.var_name in ["arr", "lst", "dict"]:
                mutations += 1
    return mutations == 0
```

2. Use in rendering:

```python
purity = analyzer.is_pure()
if not purity:
    print("\n[WARNING] This function modifies its inputs!")
```

### How to Add a New Renderer

**Example: Show most-changed variable**

1. Create function in `renderers/generic.py`:

```python
def render_most_active_variable(events):
    """Show the most frequently changing variable"""
    analyzer = BehaviorAnalyzer(events)
    var_flow = analyzer.get_variable_flow()
    
    if not var_flow["variables"]:
        return
    
    # Find most active
    most_active = max(var_flow["variables"], key=lambda v: v['changes'])
    
    _section_header("MOST ACTIVE VARIABLE")
    print(f"\n[Winner] {most_active['name']}")
    print(f"   * Changes: {most_active['changes']}")
    print(f"   * Transforms from {most_active['initial_value']} to {most_active['final_value']}")
```

2. Call in `decorators.py`:

```python
from .renderers.generic import render_most_active_variable

# In rendering pipeline:
if show_generic:
    if mode == "ascii":
        # ... other renderers ...
        render_most_active_variable(events)
```

---

## Key Insights

### Why This Architecture?

**Separation of Concerns**:
- **Tracer**: Captures what happened (not what it means)
- **Detectors**: Identify patterns (what algorithm is this?)
- **Analyzers**: Extract insights (what does it tell us?)
- **Renderers**: Format output (how to show it?)

**Benefits**:
- Easy to extend (add new detector without touching renderer)
- Easy to test (each component is independent)
- Easy to debug (each component has clear input/output)
- Easy to understand (each component does one thing)

### Data Flow Philosophy

```
Raw Events → Pattern Detection → Analysis → Formatting → Output
(What)        (Why)               (Insights)  (Presentation)
```

Each step enriches the data without modifying previous steps.

### Extension Philosophy

Add features by:
1. **New detector** - Identify new patterns
2. **New analyzer** - Extract new insights
3. **New renderer** - Display information differently

Never modify core tracer or event structure.

---

## Summary

**AlgoViz executes your function while recording every detail, then analyzes those details to understand what algorithm you're using and renders a clear explanation of how it works.**

The flow is:
1. **Decorate** function with `@visualize()`
2. **Trace** execution with `sys.settrace()`
3. **Detect** patterns by analyzing events
4. **Analyze** behavior to extract insights
5. **Render** output for display
6. **Return** original result

Each component is independent, testable, and extensible.

You can now understand, extend, and build upon this system!
