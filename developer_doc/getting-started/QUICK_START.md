# Quick Start Guide

Get started with AlgoViz in 5 minutes.

---

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/algo_viz.git
cd algo_viz

# Install in development mode
pip install -e .
```

---

## Basic Usage

### 1. Visualize Any Function

```python
from algo_viz import visualize

@visualize()
def calculate_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total

# Call the function - visualization appears automatically
result = calculate_sum(5)
print(f"Result: {result}")
```

**Output shows:**
- Algorithm trace with step-by-step execution
- Variable changes at each step
- Algorithm pattern recognition

---

### 2. Enable Generic Analysis

Shows behavior patterns in ANY function:

```python
@visualize(show_generic=True)
def find_maximum(arr):
    if not arr:
        return None
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val

result = find_maximum([3, 7, 2, 9, 1])
```

**Output shows 6 sections:**
1. **FUNCTION BEHAVIOR** - Inputs/outputs/control flow
2. **EXECUTION STATISTICS** - Event counts and metrics
3. **DETECTED PATTERNS** - Algorithms found (loops, conditionals, etc.)
4. **OPERATIONS PERFORMED** - Low-level operations (loops, branches, arithmetic)
5. **VARIABLE TRACKING** - Variables grouped by activity (high/low)
6. **DATA FLOW** - How data transforms

---

### 3. Different Rendering Modes

```python
# ASCII text (default)
@visualize(mode="ascii")

# HTML file in browser
@visualize(mode="html")

# Machine-readable JSON
@visualize(mode="json")

# Algorithm-specific (no generic)
@visualize(show_generic=False)
```

---

## Examples

### Example 1: Simple Loop

```python
@visualize(show_generic=True)
def sum_range(n):
    total = 0
    for i in range(n):
        total += i
    return total

sum_range(5)  # See loop detection, accumulation pattern, variable tracking
```

**Key sections to look at:**
- **DETECTED PATTERNS**: Shows "Loops (4x)" and "Accumulation"
- **VARIABLE TRACKING**: Shows `total` with 4 changes (0→1→3→6→10)
- **EXECUTION STATISTICS**: 8 events, 2 unique variables

---

### Example 2: Conditional Logic

```python
@visualize(show_generic=True)
def classify_number(x):
    if x < 0:
        return "negative"
    elif x == 0:
        return "zero"
    else:
        return "positive"

classify_number(5)
```

**Key sections to look at:**
- **DETECTED PATTERNS**: Shows "Conditionals (3 branches)"
- **VARIABLE TRACKING**: Shows `x` with 0 changes (constant)
- **OPERATIONS**: Shows 2 conditionals executed

---

### Example 3: Recursion

```python
@visualize(show_generic=True)
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

factorial(5)
```

**Key sections to look at:**
- **FUNCTION BEHAVIOR**: Shows "Recursion depth: 4"
- **EXECUTION STATISTICS**: Multiple function calls
- **DETECTED PATTERNS**: Shows "Recursion detected"

---

### Example 4: Array Operations

```python
@visualize(show_generic=True)
def find_duplicates(arr):
    seen = {}
    duplicates = []
    for x in arr:
        if x in seen:
            duplicates.append(x)
        else:
            seen[x] = True
    return duplicates

find_duplicates([1, 2, 2, 3, 3, 3])
```

**Key sections to look at:**
- **OPERATIONS**: Shows data structures used (dict, list)
- **DETECTED PATTERNS**: Shows loops and conditionals
- **VARIABLE TRACKING**: Shows activity of `seen` and `duplicates`

---

## Output Interpretation Quick Guide

### FUNCTION BEHAVIOR Section
**Shows:** Inputs, outputs, call depth

**Why it matters:** Understand what the function takes and returns

```
[INPUT] Arguments:
   • n: 5 (int)

[OUTPUT] Type: int

[EXECUTION]
   • Function calls: 1
   • Call depth: 1
```

---

### EXECUTION STATISTICS Section
**Shows:** Event count, variable changes, unique variables

**Why it matters:** Higher counts = more complex execution

```
[TRACE SUMMARY]
   • Total events: 10           ← Complexity indicator
   • Variable changes: 8
   • Unique variables: 2
```

---

### DETECTED PATTERNS Section
**Shows:** Recognized algorithm patterns

**Why it matters:** Quickly identify what your code does

```
[+] Loops (4x)                ← Found 4-iteration loop
    • iteration count: 4

[+] Accumulation              ← Building up a result
    • accumulator vars: total
```

---

### VARIABLE TRACKING Section
**Shows:** Variables grouped by activity level

**Why it matters:** Focus on important variables first

```
[HIGH ACTIVITY] (frequently changed):    ← Key variables
   • total: Changes: 4 | Transform: 0...→...10

[LOW ACTIVITY] (set once or twice):     ← Constants/parameters
   • n: Changes: 1 | Value: 5
```

---

### DATA FLOW Section
**Shows:** How data transforms

**Why it matters:** Understand data movement through code

```
total:
   • Starts as: 0 (int)
   • Transforms to: 4 different value(s)
```

---

## Common Scenarios

### "I want to understand this algorithm"
```python
@visualize(show_generic=True)
def their_function():
    pass
# See DETECTED PATTERNS and VARIABLE TRACKING sections
```

### "Is my function efficient?"
```python
@visualize(show_generic=True)
def my_function():
    pass
# Check EXECUTION STATISTICS total events
# Look for unnecessary loops in DETECTED PATTERNS
```

### "Where's the bug?"
```python
@visualize(show_generic=True)
def buggy_function():
    pass
# Check VARIABLE TRACKING for unexpected changes
# Check DATA FLOW for wrong transformations
```

### "What does this loop do?"
```python
@visualize(show_generic=True)
def my_function():
    pass
# Look at DETECTED PATTERNS for loop details
# Check VARIABLE TRACKING for what changes in loop
```

---

## Tips & Tricks

### 1. Compare Two Functions
```python
@visualize(show_generic=True)
def solution_v1():
    pass

@visualize(show_generic=True)
def solution_v2():
    pass

# See which uses fewer events = more efficient
```

### 2. Trace Specific Inputs
```python
@visualize(show_generic=True)
def my_function(n):
    pass

# Try different inputs to see behavior
my_function(1)   # Minimal case
my_function(10)  # Normal case
my_function(100) # Large case
```

### 3. Focus on HIGH ACTIVITY Variables
The variables that matter most show up first in VARIABLE TRACKING.
These are where the computation happens.

### 4. Combine with Print Debugging
```python
@visualize(show_generic=True)
def debug_function():
    # Add prints + visualization together
    print("Before loop")
    for i in range(5):
        print(f"Iteration {i}")
    print("After loop")
```

---

## Disabling Features

```python
# Only show algorithm-specific rendering (no generic analysis)
@visualize(show_generic=False)

# No visualization at all
@visualize(enabled=False)

# Use with specific rendering mode
@visualize(mode="ascii")  # Default
@visualize(mode="html")   # Opens browser
@visualize(mode="json")   # For parsing
```

---

## File Organization

```
algo_viz/
├── tracer/           # Execution tracing
├── detectors/        # Pattern detection (algorithm-specific & generic)
├── analyzers/        # Behavior analysis
├── renderers/        # Output formatting
└── __init__.py       # Main exports
```

---

## Learn More

- **[Rendering Guide](RENDERING_GUIDE.md)** - Detailed output explanation
- **[Generic Analysis Guide](GENERIC_ANALYSIS_GUIDE.md)** - Pattern detection details
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Extend AlgoViz
- **[Examples](examples/)** - Complete working examples

---

## Examples in Repository

Check `examples/` folder for:
- `generic_analysis_examples.py` - 12 example functions
- `two_pointers.py` - Algorithm-specific examples
- Other algorithm examples

Run any example:
```bash
python examples/generic_analysis_examples.py
```

---

## Next Steps

1. **Run the examples** - See AlgoViz in action
2. **Apply to your code** - Visualize your functions
3. **Read the guides** - Understand all features
4. **Extend it** - Add custom patterns/renderers
5. **Share findings** - Help others understand code

---

## FAQ

**Q: Does it work with all Python functions?**  
A: Yes! Generic analysis works with any Python function.

**Q: Is it slow?**  
A: Tracing adds overhead but is usually negligible for development/learning.

**Q: Can I use it in production?**  
A: Not recommended - it's for development, learning, and debugging.

**Q: Can I disable visualization for specific functions?**  
A: Yes: `@visualize(enabled=False)`

**Q: What about performance-critical code?**  
A: Use `show_generic=False` and `mode="json"` for minimal overhead.

**Q: Can I export the data?**  
A: Yes: `mode="json"` exports machine-readable format.

---

## Troubleshooting

**Problem:** Output is empty  
**Solution:** Try with more complex functions (loops, conditionals)

**Problem:** Unicode errors on Windows  
**Solution:** Update to latest version - fixed in v2.0+

**Problem:** Output is too large  
**Solution:** Try `show_generic=False` for less output

**Problem:** Can't see output  
**Solution:** Make sure `mode="ascii"` (default) and `show_generic=True`

---

Start with Example 1 above and explore from there!
