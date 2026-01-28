#!/usr/bin/env python3
"""
Examples demonstrating the new generic function analysis capabilities.
"""

from algo_viz import visualize


# ============================================================================
# EXAMPLE 1: Simple Loop and Accumulation
# ============================================================================

@visualize()
def calculate_sum(n):
    """Calculate sum of numbers from 0 to n."""
    total = 0
    for i in range(n):
        total += i
    return total


# ============================================================================
# EXAMPLE 2: Conditional Logic
# ============================================================================

@visualize()
def classify_number(x):
    """Classify a number as positive, negative, or zero."""
    if x < 0:
        return "negative"
    elif x == 0:
        return "zero"
    else:
        return "positive"


# ============================================================================
# EXAMPLE 3: Nested Loops
# ============================================================================

@visualize()
def multiply_matrices_simple(n):
    """Simulate a nested loop operation."""
    result = 0
    for i in range(n):
        for j in range(n):
            result += i * j
    return result


# ============================================================================
# EXAMPLE 4: List Operations
# ============================================================================

@visualize()
def filter_and_transform(items):
    """Filter and transform a list."""
    result = []
    for item in items:
        if item > 0:
            result.append(item * 2)
    return result


# ============================================================================
# EXAMPLE 5: Dictionary Operations
# ============================================================================

@visualize()
def create_frequency_map(items):
    """Create a frequency map of items."""
    frequency = {}
    for item in items:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1
    return frequency


# ============================================================================
# EXAMPLE 6: String Operations
# ============================================================================

@visualize()
def reverse_string(s):
    """Reverse a string."""
    result = ""
    for char in s:
        result = char + result
    return result


# ============================================================================
# EXAMPLE 7: Complex Control Flow
# ============================================================================

@visualize()
def find_value(items, target):
    """Find a value in a list with early return."""
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1


# ============================================================================
# EXAMPLE 8: Type Transformations
# ============================================================================

@visualize()
def parse_and_sum(strings):
    """Parse strings to integers and sum them."""
    total = 0
    for s in strings:
        num = int(s)
        total += num
    return total


# ============================================================================
# EXAMPLE 9: Multiple Data Structures
# ============================================================================

@visualize()
def analyze_items(items):
    """Analyze items using multiple data structures."""
    unique_items = set(items)
    item_count = {}
    for item in items:
        item_count[item] = item_count.get(item, 0) + 1
    
    return {
        "total": len(items),
        "unique": len(unique_items),
        "frequency": item_count,
    }


# ============================================================================
# EXAMPLE 10: Recursive Function
# ============================================================================

@visualize()
def fibonacci(n):
    """Calculate fibonacci number recursively."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ============================================================================
# EXAMPLE 11: Combining Loops and Conditionals
# ============================================================================

@visualize()
def bubble_sort_single_pass(arr):
    """Simulate a bubble sort pass."""
    n = len(arr)
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            # Swap
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return arr


# ============================================================================
# EXAMPLE 12: Data Processing Pipeline
# ============================================================================

@visualize()
def process_data_pipeline(data):
    """Process data through multiple stages."""
    # Stage 1: Filter
    filtered = []
    for item in data:
        if isinstance(item, (int, float)) and item > 0:
            filtered.append(item)
    
    # Stage 2: Transform
    transformed = []
    for item in filtered:
        transformed.append(item * 2)
    
    # Stage 3: Aggregate
    result = sum(transformed)
    
    return {
        "count": len(filtered),
        "sum": result,
        "average": result / len(filtered) if filtered else 0,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("AlgoViz Generic Analysis Examples")
    print("=" * 70)

    print("\n\n[EXAMPLE 1] Simple Loop and Accumulation")
    print("-" * 70)
    calculate_sum(5)

    print("\n\n[EXAMPLE 2] Conditional Logic")
    print("-" * 70)
    classify_number(5)

    print("\n\n[EXAMPLE 3] Nested Loops")
    print("-" * 70)
    multiply_matrices_simple(3)

    print("\n\n[EXAMPLE 4] List Operations")
    print("-" * 70)
    filter_and_transform([1, -2, 3, -4, 5])

    print("\n\n[EXAMPLE 5] Dictionary Operations")
    print("-" * 70)
    create_frequency_map([1, 2, 1, 3, 2, 1])

    print("\n\n[EXAMPLE 6] String Operations")
    print("-" * 70)
    reverse_string("hello")

    print("\n\n[EXAMPLE 7] Complex Control Flow")
    print("-" * 70)
    find_value([10, 20, 30, 40], 30)

    print("\n\n[EXAMPLE 8] Type Transformations")
    print("-" * 70)
    parse_and_sum(["1", "2", "3"])

    print("\n\n[EXAMPLE 9] Multiple Data Structures")
    print("-" * 70)
    analyze_items([1, 2, 1, 3, 2, 1])

    print("\n\n[EXAMPLE 10] Recursive Function")
    print("-" * 70)
    fibonacci(5)

    print("\n\n[EXAMPLE 11] Array Manipulation")
    print("-" * 70)
    bubble_sort_single_pass([3, 1, 4, 1, 5])

    print("\n\n[EXAMPLE 12] Data Processing Pipeline")
    print("-" * 70)
    process_data_pipeline([1, 2, 3, 4, 5, -1, 0])
