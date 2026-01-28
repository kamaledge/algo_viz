# Contributing to AlgoViz

Thank you for your interest in contributing to AlgoViz! We welcome contributions from everyone.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/algo-viz.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Install development dependencies: `pip install -e .`

## Running Tests

```bash
python -m pytest test_algoviz.py -v
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Keep functions focused and testable
- Add docstrings to public functions

## Areas for Contribution

### Pattern Detectors
Add new algorithm pattern detection:
- Greedy algorithms
- Graph algorithms (DFS, BFS)
- Binary search
- More pattern-specific optimizations

### Renderers
- Better HTML visualization with animations
- JSON export format
- Integration with Jupyter notebooks
- Custom themes and color schemes

### Core Improvements
- Performance optimization
- Better error messages
- Support for more Python constructs
- Documentation improvements

## Pull Request Process

1. Update tests for new features
2. Ensure all tests pass
3. Update README if adding new features
4. Add changelog entry in CHANGELOG.md
5. Submit PR with clear description

## Reporting Bugs

Use GitHub Issues with:
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Code example if possible

## Questions?

Open a discussion or issue on GitHub!

Thank you for making AlgoViz better! 🎉
