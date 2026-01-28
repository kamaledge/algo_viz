# AlgoViz Documentation Navigation Guide

This guide helps you find what you need quickly.

---

## For Different Roles

### 👤 I'm a Developer Learning This Project

**Read in this order:**

1. **[ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md)** ← **START HERE**
   - Complete end-to-end walkthrough
   - Code examples at every step
   - Data structures explained
   - Real function traced through entire system
   - **30 minutes to understand everything**

2. **[DEVELOPER_COMPLETE.md](DEVELOPER_COMPLETE.md)**
   - API reference for each component
   - How to extend with new detectors
   - How to add new analyzers
   - How to create new renderers

3. **[QUICK_START.md](QUICK_START.md)**
   - Practical examples to run
   - Output explanations
   - Testing the examples

### 👨‍💼 I'm Using AlgoViz for Learning

**Read in this order:**

1. **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
2. **[ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md)** - Understand how it works
3. Examples in `examples/` folder - See it in action

### 🔧 I Want to Extend/Contribute

**Read in this order:**

1. **[ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md)** - Understand the system
2. **[DEVELOPER_COMPLETE.md](DEVELOPER_COMPLETE.md)** - Extension points section
3. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines

---

## Quick Reference by Topic

### Understanding the System

| Topic | Where to Find | Time |
|-------|---------------|------|
| **Complete system flow** | [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md#complete-flow-diagram) | 30 min |
| **How function execution is traced** | [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md#phase-2-execution--tracing) | 10 min |
| **How patterns are detected** | [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md#phase-3-pattern-detection) | 10 min |
| **How behavior is analyzed** | [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md#phase-4-behavior-analysis) | 10 min |
| **How output is rendered** | [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md#phase-5-rendering) | 10 min |

### Using AlgoViz

| Topic | Where to Find | Time |
|-------|---------------|------|
| **Basic usage** | [QUICK_START.md](QUICK_START.md#basic-usage) | 5 min |
| **Understanding output** | [QUICK_START.md](QUICK_START.md#understanding-the-output) | 5 min |
| **Generic analysis** | [QUICK_START.md](QUICK_START.md#generic-analysis) | 10 min |
| **Examples** | [QUICK_START.md](QUICK_START.md#examples) or `examples/` folder | 15 min |

### Extending AlgoViz

| Topic | Where to Find | Time |
|-------|---------------|------|
| **Add new pattern detector** | [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md#how-to-add-a-new-detector) | 15 min |
| **Add new analyzer** | [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md#how-to-add-a-new-analyzer) | 15 min |
| **Add new renderer** | [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md#how-to-add-a-new-renderer) | 15 min |
| **Architecture details** | [DEVELOPER_COMPLETE.md](DEVELOPER_COMPLETE.md#architecture) | 20 min |
| **Best practices** | [DEVELOPER_COMPLETE.md](DEVELOPER_COMPLETE.md#best-practices) | 10 min |

### Troubleshooting

| Problem | Where to Find |
|---------|---------------|
| **Unicode/emoji errors** | [DEVELOPER_COMPLETE.md](DEVELOPER_COMPLETE.md#unicode-errors-on-windows) |
| **Missing events in trace** | [DEVELOPER_COMPLETE.md](DEVELOPER_COMPLETE.md#missing-events) |
| **Slow tracing** | [DEVELOPER_COMPLETE.md](DEVELOPER_COMPLETE.md#slow-tracing) |
| **How does this work?** | [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md) |

---

## The Core Documents

### 1. ARCHITECTURE_DEEP_DIVE.md (The Complete Reference)
**Your one-stop explanation of how AlgoViz works**

Contains:
- Complete end-to-end flow from code to output
- Step-by-step execution with real code
- How each component works with examples
- Data structures explained
- Real example traced completely
- How to extend the system

**Best for**: Understanding how everything works together

**Read time**: 30-40 minutes

**Key sections**:
- Complete Flow Diagram
- Step-by-Step Execution
- Component Deep Dive
- Real Example Walkthrough

---

### 2. DEVELOPER_COMPLETE.md (The API Reference)
**Reference guide for development**

Contains:
- Architecture overview
- Component API documentation
- Rendering architecture
- Code organization
- Performance considerations
- FAQ and troubleshooting

**Best for**: Looking up specific details, extending features

**Read time**: As needed (reference doc)

**Key sections**:
- Architecture
- File Structure
- Development Guide
- Troubleshooting

---

### 3. QUICK_START.md (Get Started)
**Practical guide with examples**

Contains:
- Installation
- Basic usage examples
- Output explanation
- Generic analysis examples
- How to run tests

**Best for**: Getting started, running examples

**Read time**: 10-15 minutes

**Key sections**:
- Installation
- 5-Minute Tutorial
- Examples

---

## How the Documents Relate

```
┌─────────────────────────────────────────────────────────┐
│ README.md - Project Overview                            │
│ "What is AlgoViz and why should I care?"               │
└────────────────┬────────────────────────────────────────┘
                 │
     ┌───────────┴───────────┬──────────────┐
     ▼                       ▼              ▼
┌─────────────┐  ┌──────────────────┐  ┌──────────────┐
│QUICK_START  │  │ARCHITECTURE      │  │DEVELOPER     │
│Get started  │  │DEEP_DIVE         │  │COMPLETE      │
│in 5 min     │  │Understand        │  │API reference │
│Examples     │  │completely        │  │How to extend │
│Running code │  │30-40 min read    │  │Troubleshoot  │
└─────────────┘  └──────────────────┘  └──────────────┘
     │                   │                    │
     └───────────────────┼────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
     ┌──────────────┐        ┌──────────────────┐
     │ CHANGELOG    │        │ CONTRIBUTING     │
     │ Version info │        │ How to contribute│
     └──────────────┘        └──────────────────┘
```

---

## Reading Recommendations by Goal

### Goal: "I just want to use this"
1. Read: [QUICK_START.md](QUICK_START.md) (10 min)
2. Run: Examples in `examples/` folder
3. Try: Your own functions with `@visualize()`

### Goal: "I want to understand how it works"
1. Read: [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md) (40 min)
2. Read: Relevant sections in [DEVELOPER_COMPLETE.md](DEVELOPER_COMPLETE.md)
3. Do: Code walkthrough of one example

### Goal: "I want to add new features"
1. Read: [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md) (40 min) ← **Essential**
2. Read: [DEVELOPER_COMPLETE.md](DEVELOPER_COMPLETE.md#development-guide)
3. Read: [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md#extension-points)
4. Try: Add a simple detector or renderer

### Goal: "I want to contribute"
1. Read: All above documents
2. Read: [CONTRIBUTING.md](CONTRIBUTING.md)
3. Read: [IMPROVEMENTS.md](IMPROVEMENTS.md) for ideas
4. Make: A pull request

---

## Key Concepts You'll Learn

### From ARCHITECTURE_DEEP_DIVE

- How `sys.settrace()` captures execution
- How events are recorded
- How patterns are detected from events
- How behavior is analyzed
- How output is rendered
- How to extend the system

### From DEVELOPER_COMPLETE

- Full API documentation
- Component interfaces
- Code organization
- Best practices
- Troubleshooting

### From QUICK_START

- How to use the library
- What the output means
- How to analyze results
- Running examples

---

## Pro Tips

1. **Read ARCHITECTURE_DEEP_DIVE first** - It ties everything together
2. **Reference DEVELOPER_COMPLETE later** - When you need specific API details
3. **Keep QUICK_START handy** - For usage examples
4. **Run examples while reading** - See theory in practice
5. **Trace through code yourself** - Pick a simple function, run it with `@visualize()`, read the output, then read the code that produced it

---

## The Foundation

Everything in AlgoViz builds on this principle:

```
Trace Execution → Detect Patterns → Analyze Behavior → Render Output
```

Once you understand this flow (from ARCHITECTURE_DEEP_DIVE), everything else makes sense.

---

## Questions This Documentation Answers

### Architecture
- "What is the overall structure?" → ARCHITECTURE_DEEP_DIVE
- "How do components interact?" → ARCHITECTURE_DEEP_DIVE
- "What data flows between components?" → ARCHITECTURE_DEEP_DIVE
- "How can I extend this?" → ARCHITECTURE_DEEP_DIVE + DEVELOPER_COMPLETE

### Usage
- "How do I use this?" → QUICK_START
- "What do the outputs mean?" → QUICK_START
- "Can I use this for my function?" → QUICK_START

### Development
- "What's the API?" → DEVELOPER_COMPLETE
- "How do I add a detector?" → ARCHITECTURE_DEEP_DIVE + DEVELOPER_COMPLETE
- "Where do I put my code?" → DEVELOPER_COMPLETE
- "What are best practices?" → DEVELOPER_COMPLETE

### Troubleshooting
- "Why is this not working?" → DEVELOPER_COMPLETE#Troubleshooting
- "What happened in my function?" → ARCHITECTURE_DEEP_DIVE (to understand the tracing)

---

## Your Learning Journey

```
START HERE ──→ Run an example ──→ Understand output ──→ Modify example
      ↓                                                       │
  Read 5-min                                                  │
  Quick Start                                                 ↓
      │                                         Read full ARCHITECTURE
      ↓                                          │
  Want to understand      NO                     │ Want to build
  how it works? ────────────────────── Done!     │ your own feature?
      │ YES                                      │
      ├────────────────────────────────────→ Read DEVELOPER_COMPLETE
      │
      ▼
  Read ARCHITECTURE_DEEP_DIVE
  (complete end-to-end flow)
      │
      ├─────────→ Understand how tracing works
      ├─────────→ Understand pattern detection
      ├─────────→ Understand behavior analysis
      ├─────────→ Understand rendering
      └─────────→ Know extension points
            │
            ↓
        Want to extend?
            │
            ├─→ Read extension points section
            ├─→ Read DEVELOPER_COMPLETE
            └─→ Code your feature!
```

---

## Summary

**For crystal-clear understanding of how AlgoViz works end-to-end:**
→ Read [ARCHITECTURE_DEEP_DIVE.md](ARCHITECTURE_DEEP_DIVE.md)

**For practical usage:**
→ Read [QUICK_START.md](QUICK_START.md)

**For development reference:**
→ Use [DEVELOPER_COMPLETE.md](DEVELOPER_COMPLETE.md)

Everything is interconnected - start with ARCHITECTURE_DEEP_DIVE and everything else will make sense!
