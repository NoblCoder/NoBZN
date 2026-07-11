<!-- @format -->

# 🚀 Quick Start Guide

## Installation

No dependencies needed! Just Python 3.7+.

```bash
cd "crossword puzzle solver"
chmod +x crossword_solver.py  # Make executable (optional)
```

## Running the Solver

### Option 1: Interactive Mode (Recommended for beginners)

```bash
python3 crossword_solver.py
```

This will guide you through:

1. Choosing how to input a puzzle (file, manual, or example)
2. Displaying the puzzle structure
3. Solving the puzzle
4. Optionally saving the solution

### Option 2: Solve from File

```bash
python3 crossword_solver.py example_puzzles/tiny_3x3.txt
```

### Option 3: Quick Demo

```bash
python3 demo.py
```

Watch the solver tackle multiple puzzles with explanations.

## Creating Puzzle Files

Create a text file (e.g., `my_puzzle.txt`):

```
# My first crossword puzzle
# Comments start with #
...
.#.
...
```

Format rules:

- `.` or `_` = empty cell (white square)
- `#` = blocked cell (black square)
- `A-Z` = pre-filled letter
- Lines starting with `#` = comments

## Command-Line Options

```bash
# Use custom dictionary
python3 crossword_solver.py puzzle.txt -d my_words.txt

# Save solution to file
python3 crossword_solver.py puzzle.txt -o solution.txt

# Quiet mode (less output)
python3 crossword_solver.py puzzle.txt -q

# Limit attempts
python3 crossword_solver.py puzzle.txt -m 100000

# Help
python3 crossword_solver.py -h
```

## Example Puzzles

Three examples are included:

| File             | Size | Difficulty | Solve Time |
| ---------------- | ---- | ---------- | ---------- |
| `tiny_3x3.txt`   | 3×3  | Easy       | < 1s       |
| `small_5x5.txt`  | 5×5  | Medium     | 1-10s      |
| `medium_7x7.txt` | 7×7  | Hard       | 10-60s     |

Try them:

```bash
python3 crossword_solver.py example_puzzles/tiny_3x3.txt
python3 crossword_solver.py example_puzzles/small_5x5.txt
python3 crossword_solver.py example_puzzles/medium_7x7.txt
```

## Testing Individual Modules

Each module has built-in tests:

```bash
python3 lexicon.py     # Test dictionary and pattern matching
python3 grid.py        # Test grid parsing and intersections
python3 solver.py      # Test the backtracking algorithm
python3 optimizations.py  # Test advanced features
```

## Troubleshooting

### "No dictionary found"

The solver tries to use `/usr/share/dict/words` by default. If not found, it uses a minimal built-in dictionary. To use your own:

```bash
python3 crossword_solver.py puzzle.txt -d /path/to/words.txt
```

### "No solution found"

This can happen if:

- The puzzle is impossible to solve
- The dictionary doesn't contain the right words
- You hit the attempt limit (increase with `-m`)

Try:

```bash
python3 crossword_solver.py puzzle.txt -m 5000000  # 5 million attempts
```

### Slow solving

For large puzzles (10×10+), solving can take minutes or hours. Tips:

- Use a smaller dictionary
- Simplify the grid layout (more black squares)
- Pre-fill some letters

## Understanding the Output

### Progress Display

```
Progress: 25.0% | Attempts: 1,234 | Backtracks: 567 | Current: 3-across
```

- **Progress**: % of slots filled
- **Attempts**: Total word placements tried
- **Backtracks**: Times the solver had to undo and try different words
- **Current**: Which slot is being filled now

### Solution Display

```
ACROSS:
  1. HELLO (5 letters)
  3. WORLD (5 letters)

DOWN:
  1. HAPPY (5 letters)
  2. LAUGH (5 letters)
```

Shows the final words for each slot.

## Tips for Creating Good Puzzles

1. **Start Small**: Begin with 3×3 or 5×5 grids
2. **Use Symmetry**: Real crosswords are usually symmetric
3. **Avoid Isolated Sections**: Make sure all words connect
4. **Balance White/Black**: More black squares = easier to solve
5. **Test First**: Verify your puzzle is solvable!

## Next Steps

- Read [README.md](README.md) for architecture details
- Modify the solver to add features
- Create your own puzzles
- Try larger dictionaries from online sources
- Implement clue understanding with NLP (advanced!)

## Getting Help

If something doesn't work:

1. Check this guide
2. Read error messages carefully
3. Try the example puzzles to verify your setup
4. Review the module tests

Happy solving! 🧩✨
