# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-28

### Added
- Initial release of AlgoViz
- Algorithm pattern detection:
  - Dynamic Programming (DP) with formula extraction
  - Two Pointers with array visualization
  - Sliding Window with window visualization
  - Recursion with call tree
- Multiple renderers:
  - ASCII terminal output
  - HTML interactive timeline
  - DP table evolution visualization
  - Recursion tree visualization
- Zero-configuration execution tracing using Python's `sys.settrace()`
- Support for Python 3.9+
- Cross-platform compatibility (Windows, Linux, macOS)

### Features
- `@visualize()` decorator for instant algorithm visualization
- Automatic variable tracking
- Formula extraction for DP algorithms
- List index change detection
- Recursion depth tracking
- Pattern-specific visualizations

### Known Limitations
- CLI is placeholder (main usage via decorator)
- Limited to single-file algorithms
- No support for multi-threaded code
- No support for generator functions

## Future

### Planned for v0.2.0
- Enhanced CLI for running standalone scripts
- JSON export for results
- Custom color themes
- Performance metrics
- More algorithm patterns (greedy, graph algorithms)
- Better HTML visualization with animations
