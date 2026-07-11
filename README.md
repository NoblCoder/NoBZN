<!-- @format -->

# 🧩 Crossword Puzzle Solver

A sophisticated Python-based crossword puzzle solver that uses **Constraint Satisfaction Problem (CSP)** techniques with backtracking and intelligent heuristics to fill crossword grids.

## 🎯 Features

- **Fast Pattern Matching**: Optimized dictionary lookups using regex and length-based grouping
- **Intelligent Solving**: Uses Minimum Remaining Values (MRV) heuristic to minimize backtracking
- **Constraint Propagation**: Validates intersections to avoid dead ends early
- **Interactive & File-Based**: Solve puzzles interactively or from text files
- **Detailed Statistics**: Track attempts, backtracks, and solving time
- **Clean Architecture**: Modular design with clear separation of concerns

## 📐 Architecture

The solver is built with four main modules, color-coded for clarity:

### 🔵 Grid Engine (`grid.py`)

**State Management & Coordinates**

- Represents the puzzle as a 2D grid
- Extracts word slots (across and down)
- Maps intersections between crossing words
- Provides efficient cell access and modification

### 🟠 Lexicon (`lexicon.py`)

**Dictionary & Pattern Matching**

- Loads and organizes words by length
- Fast pattern matching with wildcards (e.g., `B_KE_` matches BAKER, BIKES)
- Uses Python's optimized `re` module for regex matching
- Supports custom dictionaries or system word lists

### 🟢 Constraint Solver (`solver.py`)

**The Backtracking Algorithm**

- Implements backtracking with constraint satisfaction
- **MRV Heuristic**: Prioritizes slots with fewer possible words
- **Forward Checking**: Validates that intersecting slots remain solvable
- Efficient undo mechanism for fast backtracking

### 🟣 Interface (`interface.py`)

**I/O & User Experience**

- Interactive puzzle creation
- File-based puzzle loading
- Pretty-printed output with Unicode borders
- Solution export to text files

## 🚀 Quick Start

### Installation

1. Clone or download this repository
2. Ensure you have Python 3.7+ installed
3. No external dependencies required - uses Python standard library only!

```bash
cd "crossword puzzle solver"
```

### Usage

#### Interactive Mode

```bash
python crossword_solver.py
```

Follow the prompts to:

1. Choose puzzle input method (file, manual entry, or example)
2. View the puzzle structure
3. Watch the solver work
4. Optionally save the solution

#### File Mode

```bash
# Solve a puzzle from a file
python crossword_solver.py example_puzzles/tiny_3x3.txt

# Use a custom dictionary
python crossword_solver.py puzzle.txt -d my_words.txt

# Save solution to file
python crossword_solver.py puzzle.txt -o solution.txt

# Quiet mode (minimal output)
python crossword_solver.py puzzle.txt -q
```

### Puzzle File Format

Create a text file with your puzzle grid:

- Use `.` or `_` for empty cells (white squares)
- Use `#` for blocked cells (black squares)
- Use `A-Z` for pre-filled letters
- Lines starting with `#` are comments

Example (`puzzle.txt`):

```
# Simple 3x3 puzzle
...
.#.
...
```

## 📊 Example Puzzles

Three example puzzles are included:

1. **tiny_3x3.txt** - A 3×3 puzzle (perfect for testing)
2. **small_5x5.txt** - A 5×5 puzzle (moderate difficulty)
3. **medium_7x7.txt** - A 7×7 puzzle (more challenging)

Try them out:

```bash
python crossword_solver.py example_puzzles/tiny_3x3.txt
```

## 🔧 How It Works

### The Constraint Satisfaction Approach

1. **Slot Extraction**: The grid is analyzed to find all word slots and their intersections
2. **Ordering**: Slots are ordered using the MRV heuristic (slots with fewer candidates first)
3. **Backtracking**: For each slot:
   - Get all words matching the current pattern (e.g., `_A_`)
   - Try each candidate word
   - Check if intersecting slots still have valid candidates
   - If valid, recurse to next slot
   - If invalid, backtrack and try next word
4. **Solution**: When all slots are filled consistently, the puzzle is solved!

### Key Optimizations

- **Length-Based Grouping**: Words are pre-sorted by length, so the solver only searches relevant words
- **MRV Heuristic**: Always fills the most constrained slot first, dramatically reducing the search space
- **Forward Checking**: After placing a word, validates that intersecting slots still have candidates (catches dead ends early)
- **Efficient State Management**: Only saves/restores cells that were modified

## 📚 Dictionary Sources

The solver attempts to use your system's word list by default:

- **macOS/Linux**: `/usr/share/dict/words`

You can also provide a custom dictionary:

```bash
python crossword_solver.py puzzle.txt -d my_dictionary.txt
```

Dictionary file format: One word per line, alphabetic characters only.

## 🎓 Educational Value

This project demonstrates several important CS concepts:

- **Constraint Satisfaction Problems (CSP)**
- **Backtracking algorithms**
- **Heuristic search (MRV)**
- **State space search**
- **Pattern matching with regex**
- **Clean code architecture**
- **Object-oriented design in Python**

## 🧪 Testing

Each module includes a test function. Run individual modules to test them:

```bash
python lexicon.py    # Test dictionary loading and pattern matching
python grid.py       # Test grid parsing and intersection mapping
python solver.py     # Test the backtracking algorithm
```

## ⚡ Performance

Performance depends on:

- **Grid size**: Larger grids take exponentially longer
- **Dictionary size**: More words = more candidates to try
- **Grid density**: More black squares = fewer intersections = faster
- **Word patterns**: Uncommon letters (Q, X, Z) create fewer candidates

Typical solving times (with standard dictionary):

- **3×3 grid**: < 1 second
- **5×5 grid**: 1-10 seconds
- **7×7 grid**: 10-60 seconds
- **15×15 grid**: Minutes to hours (depends heavily on layout)

## 🔮 Future Enhancements

Potential improvements:

- **NLP Integration**: Use word embeddings to understand clues and suggest answers
- **Arc Consistency**: Pre-filter candidates using AC-3 algorithm
- **Parallel Search**: Use multiprocessing to explore multiple branches
- **GUI Interface**: Visual puzzle creation and solving
- **Web API**: Expose solver as a REST API
- **Learning**: Train a model on actual crossword answers to prefer common crossword words

## 📄 License

This project is provided as-is for educational purposes. Feel free to use, modify, and distribute.

## 🙏 Credits

Built with Python's amazing standard library:

- `re` for pattern matching
- `dataclasses` for clean data structures
- `collections.defaultdict` for efficient grouping
- `time` for performance tracking

---

**Happy Solving! 🧩✨**
