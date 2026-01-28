#!/usr/bin/env python3
"""Test improved variable tracking rendering."""

from algo_viz import visualize

@visualize(show_generic=True)
def calculate_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total

@visualize(show_generic=True)
def find_max(arr):
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Test 1: Loop with Accumulation")
    print("="*70)
    result1 = calculate_sum(5)
    print(f"Result: {result1}\n")

    print("\n" + "="*70)
    print("Test 2: Array with Conditional Update")
    print("="*70)
    result2 = find_max([2, 5, 1, 8, 3])
    print(f"Result: {result2}")
