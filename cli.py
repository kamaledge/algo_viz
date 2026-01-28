#!/usr/bin/env python3
"""
AlgoViz CLI - Command-line interface for algorithm visualization
"""

import sys
import argparse
from pathlib import Path


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog="algoviz",
        description="Visualize algorithm execution step-by-step",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  algoviz --version          Show version information
  algoviz --help             Show this help message
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
        help="Show version and exit",
    )

    args = parser.parse_args()

    # Currently just a placeholder - main usage is via @visualize decorator
    print(
        "AlgoViz - Algorithm Intuition Visualizer v0.1.0",
        file=sys.stderr,
    )
    print(
        "\nUsage: Use the @visualize() decorator in your Python code",
        file=sys.stderr,
    )
    print(
        "\nExample:",
        file=sys.stderr,
    )
    print(
        """
    from algo_viz import visualize
    
    @visualize()
    def my_algorithm(data):
        # Your algorithm here
        pass
    
    my_algorithm([1, 2, 3])
""",
        file=sys.stderr,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
