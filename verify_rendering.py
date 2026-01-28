#!/usr/bin/env python3
"""Quick verification of improved rendering."""

from algo_viz import visualize

@visualize(show_generic=True)
def simple_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total

if __name__ == "__main__":
    print("\n" + "="*70)
    print("VERIFICATION: Improved Rendering Output")
    print("="*70)
    result = simple_sum(4)
    print(f"\nFunction returned: {result}")
    print("\n[OK] Rendering complete - Check output above for quality improvements")
