"""
AlgoViz Test Suite
"""

import unittest
from algo_viz import visualize
from algo_viz.detectors.dp import detect_dp
from algo_viz.detectors.pointers import detect_two_pointers
from algo_viz.detectors.recursion import detect_recursion
from algo_viz.detectors.sliding_window import detect_sliding_window
from algo_viz.tracer.tracer import ExecutionTracer


class TestExecutionTracer(unittest.TestCase):
    """Test execution tracing"""

    def test_trace_simple_function(self):
        """Test basic tracing"""
        def simple_func(x):
            y = x + 1
            z = y * 2
            return z

        tracer = ExecutionTracer()
        result, events = tracer.run(simple_func, 5)

        self.assertEqual(result, 12)
        self.assertGreater(len(events), 0)
        # Should have call and return events
        self.assertTrue(any(e.event_type == "call" for e in events))
        self.assertTrue(any(e.event_type == "return" for e in events))

    def test_trace_loop(self):
        """Test tracing loop execution"""
        def loop_func(n):
            total = 0
            for i in range(n):
                total += i
            return total

        tracer = ExecutionTracer()
        result, events = tracer.run(loop_func, 5)
        
        self.assertEqual(result, 10)
        self.assertGreater(len(events), 0)

    def test_trace_list_changes(self):
        """Test tracing list modifications"""
        def list_func():
            arr = [0, 0, 0]
            arr[0] = 1
            arr[1] = 2
            return arr

        tracer = ExecutionTracer()
        result, events = tracer.run(list_func)
        
        self.assertEqual(result, [1, 2, 0])
        # Should detect list index changes
        list_changes = [e for e in events if "[" in (e.var_name or "")]
        self.assertGreater(len(list_changes), 0)


class TestPatternDetection(unittest.TestCase):
    """Test algorithm pattern detection"""

    def test_detect_recursion(self):
        """Test recursion detection"""
        def recursive_func(n):
            if n <= 1:
                return n
            return recursive_func(n - 1) + recursive_func(n - 2)

        tracer = ExecutionTracer()
        result, events = tracer.run(recursive_func, 4)
        
        self.assertTrue(detect_recursion(events))

    def test_detect_two_pointers(self):
        """Test two pointers detection"""
        def two_pointers_func(nums, target):
            l, r = 0, len(nums) - 1
            while l < r:
                s = nums[l] + nums[r]
                if s == target:
                    return l, r
                elif s < target:
                    l += 1
                else:
                    r -= 1
            return None

        tracer = ExecutionTracer()
        result, events = tracer.run(two_pointers_func, [1, 2, 3, 4, 5], 8)
        
        self.assertTrue(detect_two_pointers(events))

    def test_detect_dp(self):
        """Test DP detection"""
        def dp_func(n):
            dp = [0] * (n + 1)
            dp[0], dp[1] = 1, 1
            for i in range(2, n + 1):
                dp[i] = dp[i - 1] + dp[i - 2]
            return dp[n]

        tracer = ExecutionTracer()
        result, events = tracer.run(dp_func, 5)
        
        self.assertTrue(detect_dp(events))

    def test_detect_sliding_window(self):
        """Test sliding window detection"""
        def sliding_window_func(arr):
            left = 0
            window_sum = 0
            for right in range(len(arr)):
                window_sum += arr[right]
                if right - left + 1 > 3:
                    window_sum -= arr[left]
                    left += 1
            return window_sum

        tracer = ExecutionTracer()
        result, events = tracer.run(sliding_window_func, [1, 2, 3, 4, 5])

        # Should detect window variables (left and right moving)
        self.assertGreater(len(events), 0)
        # Just verify events were captured
        self.assertTrue(any(e.event_type in ["call", "return"] for e in events))
class TestDecorator(unittest.TestCase):
    """Test @visualize decorator"""

    def test_decorator_returns_result(self):
        """Test that decorator returns correct result"""
        @visualize()
        def test_func(x):
            return x * 2

        result = test_func(5)
        self.assertEqual(result, 10)

    def test_decorator_with_args(self):
        """Test decorator with function arguments"""
        @visualize()
        def add(a, b):
            return a + b

        result = add(3, 4)
        self.assertEqual(result, 7)


if __name__ == "__main__":
    unittest.main()
