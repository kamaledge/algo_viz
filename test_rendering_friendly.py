#!/usr/bin/env python3
"""
Test script to demonstrate the improved user-friendly rendering.
"""

from algo_viz import visualize


@visualize(show_generic=True)
def calculate_sum(n):
    """Calculate sum of numbers from 0 to n."""
    total = 0
    for i in range(n):
        total += i
    return total


@visualize(show_generic=True)
def find_max(arr):
    """Find the maximum value in an array."""
    if not arr:
        return None
    
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    
    return max_val


@visualize(show_generic=True)
def fibonacci(n):
    """Calculate fibonacci number recursively."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    print("=" * 60)
    print("TEST 1: Simple Loop and Accumulation")
    print("=" * 60)
    result1 = calculate_sum(5)
    print(f"Result: {result1}\n")

    print("\n" + "=" * 60)
    print("TEST 2: Conditional Logic and Array Search")
    print("=" * 60)
    result2 = find_max([3, 7, 2, 9, 1])
    print(f"Result: {result2}\n")

    print("\n" + "=" * 60)
    print("TEST 3: Recursion")
    print("=" * 60)
    result3 = fibonacci(4)
    print(f"Result: {result3}")
