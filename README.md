# Crossword puzzle solver

A standard-library Python crossword constraint solver. It solves intersections,
respects prefilled letters, and prevents repeated answers. Python 3.7+.

## Solve a clued puzzle

```sh
python3 crossword_solver.py example_puzzles/clued_3x3.json
python3 -m unittest discover -s tests -v
```

JSON puzzles support numbered clues and ranked-independent answer candidates:

```json
{
  "grid": ["...", ".#.", "..."],
  "clues": {
    "1-across": "Feline pet",
    "1-down": "Automobile",
    "2-down": "Number after nine",
    "3-across": "Moved quickly on foot"
  }
}
```

Slots use conventional row-major crossword numbering, shared by across and down
answers starting in the same cell. The example resolves to CAT / A#E / RAN,
with CAR and TEN down.

**Clue coverage is limited.** The offline starter bank in `clues.py` demonstrates
the workflow; this is not a general natural-language clue engine. Unknown clues
produce an actionable error rather than an unrelated dictionary fill. For your
own puzzles, provide a `clue_database` mapping clue text to lists of possible
answers, or a `candidates` mapping slot IDs to lists of possible answers. Explicit
candidates take precedence over clue lookup. Example:

```json
{
  "grid": ["....."],
  "clues": {"1-across": "French capital"},
  "candidates": {"1-across": ["PARIS"]}
}
```

Multiword candidates may contain spaces, apostrophes and hyphens; these are
removed before matching. Each candidate must have the slot's exact letter count.
Clued puzzles require coverage of every slot. Multiple consistent solutions may
exist; the first one found is returned. Candidate quality determines semantic
answer quality; intersections alone cannot prove a clue answer is correct.

## Dictionary fill-in mode

```sh
python3 crossword_solver.py puzzle.txt -d words.txt -o solution.txt
```

Text grids use `.` or `_` for blanks, `#` for blocks and A-Z for fixed letters.
Use `;` or `//` for comments. Legacy `# prose comment` lines remain supported;
rows made of grid characters, including `#..` and `###`, are preserved.
Rows must have equal widths. Every white cell must belong to an entry of at least
two letters.

A text grid has no clues: its output is a dictionary fill, not the intended
solution of a published crossword. Supply a crossword-specific word list with
`-d`; the system dictionary may contain obscure words. Without a system
word list, a small demonstration vocabulary is used. An explicitly missing or
empty dictionary is an error.

`-m N` limits placements (default 1,000,000). Failure and search exhaustion are
reported separately. Failed searches restore the original grid. `-q` suppresses
search progress. Omit the puzzle path for interactive dictionary fill-in mode.

## Implementation

- `grid.py`: validated layout, conventional slot extraction and intersections
- `lexicon.py`: dictionary loading and literal A-Z/wildcard matching
- `clues.py`: conservative offline clue lookup and candidate validation
- `solver.py`: dynamic minimum remaining values, forward checking and backtracking
- `interface.py`: text/JSON input and solution export

No external packages or network calls are required.
