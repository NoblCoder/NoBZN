#!/usr/bin/env python3
"""
Quick demonstration of the crossword solver's capabilities.
Run this to see the solver in action with various puzzles.
"""

from grid import Grid
from lexicon import Lexicon
from solver import CrosswordSolver
from optimizations import analyze_puzzle_difficulty, print_difficulty_analysis


def demo():
    """Demonstrate the crossword solver with example puzzles."""
    
    print("╔" + "═"*60 + "╗")
    print("║" + " "*14 + "🧩 CROSSWORD SOLVER DEMO 🧩" + " "*17 + "║")
    print("╚" + "═"*60 + "╝")
    print()
    
    # Load dictionary
    print("📚 Loading dictionary...")
    lexicon = Lexicon()
    try:
        lexicon.load_from_file('/usr/share/dict/words')
    except:
        print("Using minimal built-in dictionary...")
        lexicon._load_minimal_words()
    print()
    
    # Demo 1: Tiny 3x3 puzzle
    print("="*60)
    print("DEMO 1: Tiny 3×3 Puzzle")
    print("="*60)
    
    tiny_puzzle = [
        "...",
        ".#.",
        "..."
    ]
    
    grid1 = Grid(tiny_puzzle)
    print("\nInitial Grid:")
    print(grid1)
    
    solver1 = CrosswordSolver(grid1, lexicon)
    print("\nSolving...")
    success1 = solver1.solve(verbose=False)
    
    if success1:
        print("\n✅ SOLVED!")
        print(grid1)
        solver1.print_solution()
    
    input("\nPress Enter to continue to next demo...")
    
    # Demo 2: 5x5 puzzle with difficulty analysis
    print("\n" + "="*60)
    print("DEMO 2: 5×5 Puzzle with Difficulty Analysis")
    print("="*60)
    
    medium_puzzle = [
        ".....",
        ".#.#.",
        ".....",
        ".#.#.",
        "....."
    ]
    
    grid2 = Grid(medium_puzzle)
    print("\nInitial Grid:")
    print(grid2)
    
    # Analyze difficulty
    metrics = analyze_puzzle_difficulty(grid2, lexicon)
    print_difficulty_analysis(metrics)
    
    solver2 = CrosswordSolver(grid2, lexicon)
    print("\nSolving...")
    success2 = solver2.solve(verbose=True)
    
    if success2:
        print(grid2)
    
    input("\nPress Enter to see final summary...")
    
    # Summary
    print("\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)
    print("\nWhat you just saw:")
    print("  🔵 Grid Engine - Parsed puzzles and found intersections")
    print("  🟠 Lexicon - Matched patterns against 235K+ word dictionary")
    print("  🟢 Constraint Solver - Used backtracking with MRV heuristic")
    print("  ⚡ Optimizations - Analyzed puzzle difficulty")
    print()
    print("To solve your own puzzles:")
    print("  python3 crossword_solver.py                  # Interactive mode")
    print("  python3 crossword_solver.py puzzle.txt       # From file")
    print()
    print("For more information, see README.md")
    print("="*60)


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()
