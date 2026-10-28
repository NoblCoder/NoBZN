#!/usr/bin/env python3
"""
🧩 CROSSWORD PUZZLE SOLVER 🧩

A constraint satisfaction solver for crossword puzzles using backtracking
with intelligent heuristics.

Usage:
    python crossword_solver.py                    # Interactive mode
    python crossword_solver.py puzzle.txt         # Solve from file
    python crossword_solver.py -h                 # Show help

Architecture:
    🔵 Grid Engine (grid.py)       - State management & coordinates
    🟠 Lexicon (lexicon.py)         - Dictionary & pattern matching  
    🟢 Constraint Solver (solver.py) - Backtracking algorithm
    🟣 Interface (interface.py)     - I/O handling

Author: GitHub Copilot
"""

import sys
import argparse
from interface import CrosswordInterface


def main():
    """Main entry point with command-line argument parsing."""
    
    parser = argparse.ArgumentParser(
        description='Solve crossword puzzles using constraint satisfaction.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python crossword_solver.py                      # Interactive mode
  python crossword_solver.py puzzle.txt           # Solve puzzle from file
  python crossword_solver.py puzzle.txt -d words.txt  # Use custom dictionary
  python crossword_solver.py puzzle.txt -o solution.txt  # Save solution

Puzzle File Format:
  - One row per line
  - Use '.' or '_' for empty cells (white squares)
  - Use '#' for blocked cells (black squares)
  - Lines starting with '#' are treated as comments
  
  Example:
    ...
    .#.
    ...
        """
    )
    
    parser.add_argument(
        'puzzle',
        nargs='?',
        help='Path to puzzle file (if not provided, runs in interactive mode)'
    )
    
    parser.add_argument(
        '-d', '--dictionary',
        help='Path to custom dictionary file',
        default=None
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Path to save solution file',
        default=None
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode - minimal output'
    )
    
    parser.add_argument(
        '-m', '--max-attempts',
        type=int,
        default=1000000,
        help='Maximum number of word placement attempts (default: 1,000,000)'
    )
    
    args = parser.parse_args()
    if args.max_attempts < 1:
        parser.error("--max-attempts must be positive")
    
    # Create interface
    interface = CrosswordInterface()
    
    # Load dictionary
    if not args.quiet:
        print("📚 Loading dictionary...")
    if not interface.load_dictionary(args.dictionary):
        return 1
    
    # If no puzzle file provided, run interactive mode
    if not args.puzzle:
        interface.run_interactive()
        return 0
    
    # Load puzzle from file
    if not interface.load_puzzle_from_file(args.puzzle):
        return 1
    
    # Display puzzle
    if not args.quiet:
        interface.display_puzzle()
    
    # Solve
    success = interface.solve_puzzle(verbose=not args.quiet, max_attempts=args.max_attempts)
    
    # Save if requested
    if success and args.output:
        if not interface.save_solution(args.output):
            return 1
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
