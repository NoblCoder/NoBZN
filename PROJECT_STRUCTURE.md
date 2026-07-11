<!-- @format -->

# 📁 Project Structure

```
crossword puzzle solver/
│
├── 📘 README.md                 # Comprehensive documentation
├── 🚀 QUICKSTART.md             # Quick start guide
├── 📋 requirements.txt          # Dependencies (none needed!)
│
├── 🎯 Core Modules
│   ├── 🟠 lexicon.py            # Dictionary & pattern matching
│   ├── 🔵 grid.py               # Grid state management
│   ├── 🟢 solver.py             # Constraint satisfaction solver
│   └── 🟣 interface.py          # I/O and user interface
│
├── ⚡ Advanced Features
│   └── optimizations.py         # Heuristics & performance tools
│
├── 🎮 Entry Points
│   ├── crossword_solver.py      # Main CLI application
│   └── demo.py                  # Interactive demonstration
│
└── 📂 example_puzzles/
    ├── tiny_3x3.txt             # 3×3 puzzle (easy)
    ├── small_5x5.txt            # 5×5 puzzle (medium)
    └── medium_7x7.txt           # 7×7 puzzle (hard)
```

## Module Dependencies

```
crossword_solver.py
    └── interface.py
            ├── grid.py
            ├── lexicon.py
            └── solver.py
                    ├── grid.py
                    └── lexicon.py

demo.py
    ├── grid.py
    ├── lexicon.py
    ├── solver.py
    │       ├── grid.py
    │       └── lexicon.py
    └── optimizations.py
            ├── grid.py
            └── lexicon.py
```

## Lines of Code by Module

| Module                | Lines      | Purpose                                 |
| --------------------- | ---------- | --------------------------------------- |
| `lexicon.py`          | ~180       | Word dictionary and pattern matching    |
| `grid.py`             | ~340       | Grid representation and slot extraction |
| `solver.py`           | ~270       | Backtracking constraint solver          |
| `interface.py`        | ~320       | User interface and I/O                  |
| `optimizations.py`    | ~350       | Advanced heuristics and profiling       |
| `crossword_solver.py` | ~100       | CLI entry point                         |
| `demo.py`             | ~120       | Interactive demo                        |
| **Total**             | **~1,680** | Complete solver system                  |

## Key Classes

### 🟠 Lexicon Module

- `Lexicon` - Dictionary manager with pattern matching

### 🔵 Grid Module

- `Grid` - Grid state and cell management
- `Slot` - Represents a word slot (dataclass)
- `Intersection` - Represents crossing words (dataclass)
- `Direction` - ACROSS or DOWN (enum)

### 🟢 Solver Module

- `CrosswordSolver` - Main constraint satisfaction solver

### 🟣 Interface Module

- `CrosswordInterface` - User interaction layer

### ⚡ Optimizations Module

- `PerformanceProfiler` - Track solving metrics
- `WordFrequencyScorer` - Score words by letter frequency
- `AdvancedHeuristics` - Additional solving strategies

## Data Flow

```
1. Input
   └── Text file or manual entry
       └── interface.py parses input

2. Grid Creation
   └── grid.py builds grid representation
       ├── Extracts word slots
       └── Maps intersections

3. Dictionary Loading
   └── lexicon.py loads words
       └── Groups by length for fast lookup

4. Solving
   └── solver.py runs backtracking
       ├── Orders slots by MRV heuristic
       ├── For each slot:
       │   ├── Gets pattern from grid
       │   ├── Finds matching words from lexicon
       │   ├── Tries each candidate
       │   └── Validates intersections
       └── Returns solution or backtracks

5. Output
   └── interface.py displays result
       ├── Shows filled grid
       └── Lists all words
```

## Algorithm Complexity

- **Space**: O(N × M) for grid + O(W) for dictionary
  - N, M = grid dimensions
  - W = number of words in dictionary

- **Time**: O(W^S) worst case, but heavily pruned
  - S = number of slots
  - Heuristics reduce effective branching factor dramatically

## File Formats

### Input Puzzle (`.txt`)

```
# Comments start with #
.....    # Dots = empty cells
.#.#.    # Hash = blocked cells
.....
```

### Output Solution (`.txt`)

```
CROSSWORD SOLUTION

Grid:
A A L I I
A # L # I
B U L L A

ACROSS:
  1. AALII (5 letters)
  ...
```

## Testing

Each module includes a `test_*()` function at the bottom:

- Run `python3 <module>.py` to test
- All tests use minimal built-in dictionaries
- No external dependencies required

## Customization Points

Want to extend the solver? Start here:

1. **Custom dictionary**: Modify `Lexicon.load_from_file()`
2. **New heuristics**: Add to `AdvancedHeuristics` class
3. **Better UI**: Enhance `CrosswordInterface`
4. **Clue understanding**: Add NLP in new module
5. **GUI**: Create separate module using tkinter/PyQt
6. **Web API**: Wrap solver in Flask/FastAPI

## Performance Tips

For faster solving:

- Use smaller dictionaries (filter common words)
- Add more black squares (fewer intersections)
- Pre-fill difficult letters (Q, X, Z)
- Increase max attempts limit
- Use word frequency scoring (in optimizations.py)
