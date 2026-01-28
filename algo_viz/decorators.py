# algo_viz/decorators.py

from .tracer.tracer import ExecutionTracer
from .detectors.pointers import detect_two_pointers
from .detectors.dp import detect_dp
from .detectors.recursion import detect_recursion
from .renderers.ascii import render
from .renderers.recursion_tree import render_recursion_tree
from .renderers.html import render_html
from .detectors.sliding_window import detect_sliding_window
from .analyzers.dp import analyze_dp
from .renderers.dp_ascii import render_dp
from .renderers.two_pointers import render_two_pointers
from .renderers.sliding_window import render_sliding_window
from .detectors.generic import GenericPatternDetector
from .detectors.operations import (
    detect_for_loops,
    detect_while_loops,
    detect_if_else,
    detect_list_operations,
    detect_accumulation,
)
from .renderers.generic import (
    render_behavior_summary,
    render_variable_tracking,
    render_pattern_summary,
    render_operation_summary,
    render_execution_stats,
    render_data_flow,
)


def visualize(mode="ascii", show_generic=True):
    """
    Visualize algorithm execution with support for both specialized patterns and generic analysis.
    
    Args:
        mode: "ascii" (default), "html", or "json"
        show_generic: If True, show generic behavior analysis in addition to specialized patterns
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            tracer = ExecutionTracer()
            result, events = tracer.run(func, *args, **kwargs)

            detected_patterns = []
            
            # Detect specialized algorithm patterns
            if detect_recursion(events):
                detected_patterns.append("Recursion")
                
            if detect_sliding_window(events):
                detected_patterns.append("Sliding Window")

            if detect_two_pointers(events):
                detected_patterns.append("Two Pointers")

            if detect_dp(events):
                detected_patterns.append("Dynamic Programming")
                try:
                    dp_updates = analyze_dp(events)
                    if dp_updates:
                        render_dp(dp_updates)
                except Exception as e:
                    pass
            
            # Detect generic patterns
            generic_detector = GenericPatternDetector(events)
            generic_patterns = generic_detector.get_summary()
            
            # Detect specific operations
            operations = {
                "loops": {
                    "for": detect_for_loops(events),
                    "while": detect_while_loops(events),
                },
                "conditionals": detect_if_else(events),
                "list_operations": detect_list_operations(events),
                "accumulation": detect_accumulation(events),
            }
            
            if detected_patterns:
                print("[*] Detected Algorithm Patterns: " + ", ".join(detected_patterns))
            
            # Render generic analysis if enabled
            if show_generic:
                if mode == "ascii":
                    # Render in logical order: Summary -> Stats -> Patterns -> Operations -> Variables -> Data Flow
                    render_behavior_summary(events)
                    render_execution_stats(events)
                    
                    # Show detected patterns
                    if generic_patterns:
                        render_pattern_summary(generic_patterns)
                    
                    # Show operations performed
                    if any(operations.values()):
                        render_operation_summary(operations)
                    
                    # Show variable tracking
                    render_variable_tracking(events)
                    
                    # Show data flow
                    render_data_flow(events)

            if mode == "ascii":
                # Render specialized visualizations for each pattern
                if detect_sliding_window(events):
                    render_sliding_window(events)
                elif detect_two_pointers(events):
                    render_two_pointers(events)
                
                render(events)
                if detect_recursion(events):
                    render_recursion_tree(events)
            elif mode == "html":
                render_html(events)

            return result
        return inner
    return wrapper
