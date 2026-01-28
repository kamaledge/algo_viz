# AlgoViz Complete Developer Guide

This guide covers architecture, development, and extending AlgoViz.

---

## Quick Links

- **Getting Started**: See [QUICK_START.md](QUICK_START.md)
- **User Guide**: See [README.md](README.md)
- **API Reference**: [Architecture](#architecture) section below
- **Extending**: [Development Guide](#development-guide) section
- **Rendering System**: [Rendering Architecture](#rendering-architecture) section

---

## Architecture

### System Overview

```
@visualize() Decorator
     ↓
Execution Tracer (captures function execution)
     ↓
Pattern Detectors (identifies algorithms)
     ↓
Behavior Analyzer (extracts insights)
     ↓
Rendering Pipeline (formats output)
     ↓
Console/HTML/JSON Output
```

### Core Components

#### 1. Tracer (tracer/tracer.py)
**Purpose**: Capture function execution details

**Features**:
- Uses `sys.settrace()` to hook function calls
- Records variable changes with old/new values
- Tracks line execution and return values
- Captures source code for rendering
- Handles recursion with call stack tracking

**Key Methods**:
- `run(func, args, kwargs)` - Execute and trace function
- `get_events()` - Get all captured events
- `get_source()` - Get source code snippet

**Event Types**:
- `call` - Function called
- `return` - Function returned
- `var_change` - Variable assignment
- `exception` - Error raised

#### 2. Detectors (detectors/)
**Purpose**: Identify algorithm patterns

**Specialized Detectors**:
- `detect_recursion()` - Recursive function patterns
- `detect_dp()` - Dynamic programming patterns
- `detect_two_pointers()` - Two-pointer algorithms
- `detect_sliding_window()` - Sliding window patterns

**Generic Detector** (detectors/generic.py):
- `GenericPatternDetector` - Detects ANY pattern
- Identifies loops, conditionals, data structures
- Works on any function, not just specific algorithms

#### 3. Analyzers (analyzers/)
**Purpose**: Extract insights from traces

**DP Analyzer** (analyzers/dp.py):
- Detects DP formula patterns
- Identifies memoization usage
- Extracts state transitions

**Behavior Analyzer** (analyzers/behavior.py):
- Extracts I/O information
- Analyzes control flow
- Tracks variable transformations
- Computes complexity indicators

#### 4. Renderers (renderers/)
**Purpose**: Format output for display

**Specialized Renderers**:
- `render()` - Generic ASCII algorithm trace
- `render_dp()` - Dynamic programming trace
- `render_two_pointers()` - Two-pointer algorithm
- `render_recursion_tree()` - Recursion visualization
- `render_html()` - HTML/browser output

**Generic Renderers** (renderers/generic.py):
- `render_behavior_summary()` - Function behavior overview
- `render_execution_stats()` - Trace statistics
- `render_variable_tracking()` - Variable state changes
- `render_pattern_summary()` - Detected patterns
- `render_operation_summary()` - Operations performed
- `render_data_flow()` - Variable transformations

---

## Rendering Architecture

### Output Pipeline

When `@visualize(show_generic=True)` is used:

```
1. render_behavior_summary()     ← What does function do?
2. render_execution_stats()       ← How much activity?
3. render_pattern_summary()       ← What patterns detected?
4. render_operation_summary()     ← What operations?
5. render_variable_tracking()     ← How do variables change?
6. render_data_flow()             ← Variable transformation paths
```

### Rendering Order Principles

- **General to Specific**: Summary first, details after
- **High-Level to Low-Level**: Patterns before operations
- **Input to Output**: What comes in, what happens, what comes out

### Variable Tracking Output Example

```
VARIABLE TRACKING
============================================================

[HIGH ACTIVITY] (frequently changed):

   [total]
      * State changes: 10
      * Transforms from 0 to 55
      * Takes 11 distinct value(s)

[LOW ACTIVITY] (set once or twice):

   [n]
      * State changes: 1
      * Final value: 5
```

**Information Provided**:
- Activity categorization (how frequently changed)
- Number of state changes
- Value transformation path (start → end)
- Value diversity (how many distinct values)
- Type conversions (if applicable)

---

## Development Guide

### Adding a New Pattern Detector

#### 1. Create Detector Function

File: `detectors/your_pattern.py`

```python
def detect_your_pattern(events) -> bool:
    """Detect your pattern in execution events."""
    for event in events:
        # Your detection logic
        if event.event_type == "var_change":
            # Check for pattern
            pass
    return True  # Pattern found
```

#### 2. Register in Decorator

File: `decorators.py`

```python
from .detectors.your_pattern import detect_your_pattern

# In visualize() wrapper:
if detect_your_pattern(events):
    print("[*] Detected Your Pattern")
```

#### 3. Add Specialized Renderer (Optional)

File: `renderers/your_pattern.py`

```python
def render_your_pattern(events) -> None:
    """Render your pattern visualization."""
    print("\n[*] Your Pattern Visualization")
    # Your rendering logic
```

#### 4. Hook Renderer in Decorator

```python
if detect_your_pattern(events) and mode == "ascii":
    render_your_pattern(events)
```

### Adding a New Generic Analysis

Use the generic rendering pipeline. No new detector needed!

#### 1. Add Analysis to Behavior Analyzer

File: `analyzers/behavior.py`

```python
def analyze_your_aspect(self) -> dict:
    """Analyze your aspect of function behavior."""
    # Process self.events
    return {"insights": []}
```

#### 2. Create New Renderer Function

File: `renderers/generic.py`

```python
def render_your_analysis(events) -> None:
    """Render your analysis."""
    from algo_viz.analyzers.behavior import BehaviorAnalyzer
    
    analyzer = BehaviorAnalyzer(events)
    analysis = analyzer.analyze_your_aspect()
    
    _section_header("YOUR ANALYSIS")
    # Display analysis
```

#### 3. Add to Rendering Pipeline

File: `decorators.py`

```python
from .renderers.generic import render_your_analysis

if show_generic:
    if mode == "ascii":
        # ... other renderers ...
        render_your_analysis(events)
```

### Best Practices

#### Code Organization
- **One concern per function** - Each function does one thing
- **Use helpers** - `_section_header()` for consistent formatting
- **Avoid duplication** - Extract common patterns into functions

#### Event Processing
- **Single pass preferred** - O(n) not O(n²)
- **Early returns** - Check for data before rendering
- **Type safety** - Validate event types before accessing fields

#### Output Formatting
- **ASCII only** - No Unicode/emoji (breaks on Windows)
- **Consistent indentation** - Use 3-space bullets
- **Clear labels** - Use `[SECTION]` format for clarity
- **Scannable** - Group related info, use bullet points

#### Example Renderer Template

```python
def render_my_analysis(events) -> None:
    """Render my analysis of function execution."""
    from algo_viz.analyzers.behavior import BehaviorAnalyzer
    
    # Get analysis
    analyzer = BehaviorAnalyzer(events)
    data = analyzer.get_my_data()
    
    # Skip if no data
    if not data:
        return
    
    # Render header
    _section_header("MY ANALYSIS")
    
    # Render content
    print("\n[SUMMARY]")
    print(f"   * Items found: {len(data)}")
    
    # Render details
    for item in sorted(data, key=lambda x: x['importance'], reverse=True):
        print(f"\n   [{item['name']}]")
        print(f"      * Value: {item['value']}")
```

### Testing Your Changes

#### Unit Test

```python
def test_my_feature():
    from algo_viz.tracer.tracer import ExecutionTracer
    
    def sample_func(n):
        x = 0
        for i in range(n):
            x += i
        return x
    
    tracer = ExecutionTracer()
    result = tracer.run(sample_func, args=(5,))
    events = tracer.events
    
    # Test your detector/renderer
    assert len(events) > 0
```

#### Integration Test

```python
from algo_viz import visualize

@visualize(show_generic=True)
def test_func(n):
    return sum(range(n))

# Run and verify
result = test_func(5)
assert result == 10
```

---

## File Structure

```
algo_viz/
├── __init__.py              # Package exports
├── decorators.py            # @visualize() decorator
├── tracer/
│   ├── tracer.py           # ExecutionTracer
│   └── events.py           # Event classes
├── detectors/
│   ├── generic.py          # GenericPatternDetector
│   ├── operations.py       # Operation detection functions
│   ├── dp.py               # Dynamic programming
│   ├── recursion.py        # Recursion detection
│   ├── pointers.py         # Two-pointer detection
│   └── sliding_window.py    # Sliding window detection
├── analyzers/
│   ├── behavior.py         # BehaviorAnalyzer
│   ├── dp.py               # DP formula extraction
│   └── events.py           # Event analysis
├── renderers/
│   ├── generic.py          # Generic renderers (6 functions)
│   ├── ascii.py            # ASCII trace rendering
│   ├── dp.py               # DP visualization
│   ├── dp_ascii.py         # DP ASCII rendering
│   ├── two_pointers.py     # Two-pointer visualization
│   ├── recursion_tree.py   # Recursion tree rendering
│   ├── sliding_window.py    # Sliding window visualization
│   ├── html.py             # HTML output
│   └── json.py             # JSON export
└── __pycache__/            # Compiled Python files
```

---

## Data Flow Examples

### Simple Function Trace

```python
@visualize(show_generic=True)
def add(a, b):
    return a + b

add(3, 5)
```

**Output shows**:
- Input: a=3, b=5
- Output: int
- Operations: Arithmetic
- Data flow: 3,5 → 8

### Complex Function

```python
@visualize(show_generic=True)
def find_max(arr):
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val

find_max([3, 7, 2, 9, 1])
```

**Output shows**:
- Input: arr=[3,7,2,9,1]
- Patterns: Loop, Conditional
- HIGH ACTIVITY: max_val (4 changes: 3→7→9)
- LOW ACTIVITY: x (5 changes, just iteration)
- Data flow: max_val transforms 3→9

---

## Performance Considerations

### Tracer Overhead
- Minimal: ~10-20% overhead for tracing
- Scales linearly with function complexity
- Not suitable for performance-critical code

### Memory Usage
- Events list grows with execution
- Typical functions: <1MB for events
- Large loops: Can grow to 10MB+

### Optimization Tips
- Use limited input sizes for visualization
- Don't visualize performance-critical loops
- Filter events if rendering large traces

---

## Troubleshooting

### Unicode Errors on Windows
**Problem**: `UnicodeEncodeError` with special characters

**Solution**: Use ASCII only
```python
# Good:
print("   * Item")    # Asterisk

# Bad:
print("   • Item")    # Bullet (fails on Windows)
```

### Missing Events
**Problem**: Important variable changes not shown

**Solution**: Check event type and variable name
```python
for e in events:
    if e.event_type == "var_change" and e.var_name == "x":
        print(f"Event: {e}")
```

### Slow Tracing
**Problem**: Function takes too long to trace

**Solution**: Use smaller inputs or limit scope
```python
@visualize()
def slow_func(n):  # Don't use n=1000000
    return sum(range(n))

slow_func(100)  # Use smaller input
```

---

## Contributing

### Before Submitting Changes
1. Test with `python test_algoviz.py`
2. Check for Unicode issues
3. Verify all renderers work
4. Update documentation

### Code Style
- PEP 8 compliant
- Type hints where possible
- Docstrings for all public functions
- Comments for complex logic

### Pull Request Checklist
- [ ] Tests pass
- [ ] No Unicode hardcoding
- [ ] Documentation updated
- [ ] Code follows style guide
- [ ] Changes are self-contained

---

## FAQ

**Q: How do I add a new algorithm pattern?**  
A: Create a detector in `detectors/your_pattern.py`, register it in `decorators.py`, and optionally add a specialized renderer.

**Q: Can I use this on any function?**  
A: Yes! The generic analysis works on any function. Specialized renderers work best on specific algorithms.

**Q: How do I export data?**  
A: Use `@visualize(mode="json")` for JSON export, or implement a custom renderer.

**Q: Is this production-safe?**  
A: Not for performance-critical code (adds tracing overhead), but safe for learning/debugging.

**Q: How much does tracing slow things down?**  
A: Typically 10-20% overhead for simple functions, more for complex ones.

---

## Resources

- **Python sys.settrace()**: https://docs.python.org/3/library/sys.html#sys.settrace
- **AST Module**: https://docs.python.org/3/library/ast.html
- **Inspect Module**: https://docs.python.org/3/library/inspect.html

---

## Summary

AlgoViz is designed to be:
- **Extensible** - Easy to add new detectors and renderers
- **Maintainable** - Clear separation of concerns
- **User-Friendly** - Simple decorator-based API
- **Educational** - Shows algorithm execution clearly

The architecture prioritizes clarity and extensibility over performance.
