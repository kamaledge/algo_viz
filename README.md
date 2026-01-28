# 🧠 AlgoViz — Algorithm Intuition Visualizer

> **See your algorithm think.**

AlgoViz is a Python library that **executes your algorithm and visualizes how it evolves step by step** — pointer movement, recursion trees, sliding windows, dynamic programming state changes, AND **generic function behavior patterns** — all without print-debugging or heavyweight debuggers.

Perfect for:
- 📚 Learning algorithms
- 🎯 Interview prep (LeetCode-style)
- 👩‍🏫 Teaching & explanations
- 👀 Code reviews and intuition building
- 🔍 Understanding ANY function's behavior

---

## Documentation

📖 **[See user documentation in docs/ directory](docs/README.md)**  
👨‍💻 **[See developer documentation in developer_doc/ directory](developer_doc/README.md)**

### Quick Start for Users
1. **[docs/project/CHANGELOG.md](docs/project/CHANGELOG.md)** - Version history
2. **[docs/project/CONTRIBUTING.md](docs/project/CONTRIBUTING.md)** - How to contribute

### For Developers & Contributors
1. **[developer_doc/START_HERE.md](developer_doc/START_HERE.md)** (5 min) - Orientation
2. **[developer_doc/architecture/ARCHITECTURE_DEEP_DIVE.md](developer_doc/architecture/ARCHITECTURE_DEEP_DIVE.md)** (40 min) - **Complete system explanation**
3. **[developer_doc/getting-started/QUICK_START.md](developer_doc/getting-started/QUICK_START.md)** (10 min) - Practical examples

---

## ✨ Why AlgoViz?

| Tool | What it shows |
|----|----|
| Debugger | What happened |
| Profiler | How long it took |
| **AlgoViz** | **Why it happened** |

AlgoViz focuses on **algorithmic patterns and state evolution**, not just execution.

---

## � Installation

```bash
pip install algo-viz
```

**Requirements:**
- Python 3.9+
- Zero external dependencies!

---

## 🚀 Quick Start

### Example 1: Two Pointers Algorithm

```python
from algo_viz import visualize

@visualize()
def two_sum(nums, target):
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        if s == target:
            return l, r
        elif s < target:
            l += 1
        else:
            r -= 1

two_sum([1, 2, 3, 4, 5], 8)
```

**Output:**
```
[*] Detected patterns: Two Pointers

[*] Two Pointers Visualization
----------------------------------------------------------------------

Array: [1, 2, 3, 4, 5]

Step 1: [1] [2](l) [3] [4] [5](r)
  l=1 r=4

Step 2: [1] [2] [3](l) [4] [5](r)
  l=2 r=4

[*] Algorithm Trace
----------------------------------------
Step 02 | line 6 | l: 0 -> 1
Step 03 | line 8 | s: 6 -> 7
Step 04 | line 6 | l: 1 -> 2
```

### Example 2: Dynamic Programming

```python
from algo_viz import visualize

@visualize()
def climbing_stairs(n):
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]

climbing_stairs(5)
```

**Output:**
```
[*] Detected patterns: Dynamic Programming

[*] DP Table Evolution
--------------------------------------------------
Step 01 | Line 7 | dp[0] = 1
Step 02 | Line 7 | dp[1] = 1
Step 03 | Line 7 | dp[2] = dp[i - 1]=1 + dp[i - 2]=1 -> 2
Step 04 | Line 7 | dp[3] = dp[i - 1]=2 + dp[i - 2]=1 -> 3
Step 05 | Line 7 | dp[4] = dp[i - 1]=3 + dp[i - 2]=2 -> 5
```

### Example 3: Recursion

```python
from algo_viz import visualize

@visualize()
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(4)
```

**Output:**
```
[*] Detected patterns: Recursion

[*] Recursion Tree
----------------------------------------
[+] fibonacci(n=4)
  [+] fibonacci(n=3)
    [+] fibonacci(n=2)
      [+] fibonacci(n=1)
      [-] return 1
      [+] fibonacci(n=0)
      [-] return 0
    [-] return 1
    ...
```

---

## 🔍 Supported Patterns

### ✅ Dynamic Programming
- Automatically detects DP patterns
- Shows formula dependencies: `dp[i] = dp[i-1] + dp[i-2]`
- Visualizes DP table evolution

### ✅ Two Pointers  
- Visualizes pointer positions in array
- Shows pointer movement step-by-step
- Marks current positions clearly

### ✅ Sliding Window
- Shows window boundaries
- Visualizes element inclusion/exclusion
- Tracks window size changes

### ✅ Recursion / DFS
- Call tree visualization
- Shows function arguments
- Tracks call depth and returns

---

## 🎨 Output Modes

### ASCII (Default)
```python
@visualize(mode="ascii")
def my_algorithm(data):
    pass
```
Terminal-friendly output with step-by-step trace.

### HTML
```python
@visualize(mode="html")
def my_algorithm(data):
    pass
```
Generates `algo_viz.html` with interactive timeline visualization.

---

## 🛠 API Reference

### @visualize Decorator

```python
@visualize(mode="ascii")
def algorithm(data):
    """Visualize algorithm execution"""
    pass
```

**Parameters:**
- `mode` (str): Output format - `"ascii"` (default) or `"html"`

**Features:**
- Zero configuration required
- Automatic pattern detection
- Works with any Python function
- No code modifications needed

---

## 📖 Documentation

AlgoViz now includes **generic function analysis** in addition to algorithm visualization:

- **[QUICK_START_GENERIC.md](QUICK_START_GENERIC.md)** - Get started in 5 minutes
- **[GENERIC_ANALYSIS.md](GENERIC_ANALYSIS.md)** - Complete feature guide
- **[DEVELOPER_GENERIC.md](DEVELOPER_GENERIC.md)** - Extension & API reference
- **[UPGRADE_GUIDE.md](UPGRADE_GUIDE.md)** - Backward compatibility info

---

## ⚙️ How It Works

AlgoViz uses Python's built-in `sys.settrace()` to:
1. **Trace** function execution at the bytecode level
2. **Capture** variable assignments and changes
3. **Detect** algorithmic patterns automatically
4. **Extract** formulas and dependencies
5. **Render** step-by-step visualizations

No AST rewriting, no bytecode manipulation - pure runtime tracing!

---

## 🚀 Features

- ✅ Zero-configuration execution tracing
- ✅ Automatic algorithm pattern detection
- ✅ Step-by-step visualization
- ✅ ASCII and HTML renderers
- ✅ Python-native (runtime-based, no AST rewriting)
- ✅ Zero external dependencies
- ✅ Cross-platform (Windows, Linux, macOS)
- ✅ Works with LeetCode problems out of the box

---

## 🔧 Advanced Usage

### Custom Visualization

Extend AlgoViz by importing pattern detectors:

```python
from algo_viz.tracer.tracer import ExecutionTracer
from algo_viz.detectors.dp import detect_dp

def my_algorithm(data):
    # your code
    pass

tracer = ExecutionTracer()
result, events = tracer.run(my_algorithm, data)

if detect_dp(events):
    print("DP pattern detected!")
```

---

## 📝 Examples

The [examples/](examples/) directory contains ready-to-run demonstrations:

- `70_climbingStairs.py` - Dynamic Programming
- `two_pointers.py` - Two Pointer Technique
- `50_fibonacci.py` - Recursion
- `longestSubstringWithoutRepeatedCharacters.py` - Sliding Window

Run any example:
```bash
python examples/70_climbingStairs.py
```

---

## ⚠️ Limitations

- Single-threaded algorithms only
- No support for generator functions
- Limited to algorithm-style code (not general-purpose debugging)
- Overhead is significant for performance-critical code

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- More algorithm pattern detectors
- Additional visualization formats
- Performance optimizations
- Documentation improvements

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🎓 Learning Resources

- [Algorithm Visualizations](https://visualgo.net/) - Complementary tool for understanding algorithms
- [LeetCode](https://leetcode.com/) - Practice problems
- [GeeksforGeeks](https://www.geeksforgeeks.org/) - Algorithm tutorials

---

## 💬 Feedback

Have ideas or found bugs? Open an issue on [GitHub](https://github.com/yourusername/algo-viz)!


AlgoViz helps you:

- see pointer movement
- feel recursion
- understand state changes

If AlgoViz helped you, consider giving it a ⭐

---

## ⚠️ Notes

- Pattern detection is heuristic-based
- Visualization depends on executed inputs
- Designed for learning and intuition, not formal verification
