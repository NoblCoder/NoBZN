"""
🟣 INTERFACE MODULE (I/O)
Handles input parsing and output formatting for the crossword solver.
"""

import os
from typing import List, Optional
from grid import Grid
from lexicon import Lexicon
from solver import CrosswordSolver


class CrosswordInterface:
    """
    Provides user-friendly interface for the crossword solver.
    """
    
    def __init__(self):
        self.lexicon = Lexicon()
        self.grid = None
        self.solver = None
    
    def load_dictionary(self, filepath: Optional[str] = None) -> bool:
        """
        Load the word dictionary.
        
        Args:
            filepath: Path to dictionary file. If None, tries system default.
            
        Returns:
            True if successful
        """
        try:
            if filepath:
                self.lexicon.load_from_file(filepath)
            else:
                # Try system paths
                self.lexicon._load_system_words()
            return True
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            return False
    
    def load_puzzle_from_file(self, filepath: str) -> bool:
        """
        Load a puzzle from a text file.
        
        File format:
            - One row per line
            - Use '.' or '_' for empty cells
            - Use '#' for blocked cells
            - Use 'A'-'Z' for pre-filled letters
            - Lines starting with '#' are treated as comments
        
        Example:
            # Comment line
            ...
            .#.
            ...
        
        Args:
            filepath: Path to puzzle file
            
        Returns:
            True if successful
        """
        try:
            with open(filepath, 'r') as f:
                lines = []
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comment lines
                    if line and not line.startswith('#'):
                        lines.append(line)
            
            if not lines:
                print("Error: No puzzle data found in file.")
                return False
            
            self.grid = Grid(lines)
            print(f"✓ Loaded puzzle: {self.grid.rows}x{self.grid.cols}")
            return True
        except FileNotFoundError:
            print(f"Error: Puzzle file '{filepath}' not found.")
            return False
        except Exception as e:
            print(f"Error loading puzzle: {e}")
            return False
    
    def create_puzzle_interactive(self) -> bool:
        """
        Create a puzzle interactively through command-line prompts.
        
        Returns:
            True if successful
        """
        print("\n" + "="*60)
        print("CREATE CROSSWORD PUZZLE")
        print("="*60)
        print("\nEnter your puzzle grid row by row.")
        print("  • Use '.' or '_' for empty cells (white squares)")
        print("  • Use '#' for blocked cells (black squares)")
        print("  • Use 'A'-'Z' for pre-filled letters")
        print("  • Press Enter on an empty line when done")
        print("\nExample 3x3 puzzle:")
        print("  ...")
        print("  .#.")
        print("  ...")
        print()
        
        rows = []
        row_num = 1
        
        while True:
            try:
                line = input(f"Row {row_num}: ").strip()
                
                if not line:
                    if rows:
                        break
                    else:
                        print("  Please enter at least one row.")
                        continue
                
                # Validate characters
                valid_chars = set('._#' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + 'abcdefghijklmnopqrstuvwxyz')
                if not all(c in valid_chars for c in line):
                    print("  Invalid characters. Use only: . _ # A-Z")
                    continue
                
                # Check width consistency
                if rows and len(line) != len(rows[0]):
                    print(f"  Error: All rows must have the same width (expected {len(rows[0])}, got {len(line)})")
                    continue
                
                rows.append(line)
                row_num += 1
                
            except (EOFError, KeyboardInterrupt):
                print("\n\nCancelled.")
                return False
        
        try:
            self.grid = Grid(rows)
            print(f"\n✓ Created puzzle: {self.grid.rows}x{self.grid.cols}")
            print(f"✓ Found {len(self.grid.slots)} word slots")
            return True
        except Exception as e:
            print(f"\nError creating puzzle: {e}")
            return False
    
    def display_puzzle(self) -> None:
        """Display the current puzzle state."""
        if not self.grid:
            print("No puzzle loaded.")
            return
        
        print("\n" + "="*60)
        print("CURRENT PUZZLE")
        print("="*60)
        print(self.grid)
        
        print(f"\nSlots ({len(self.grid.slots)}):")
        
        # Group by across/down
        across_slots = {k: v for k, v in self.grid.slots.items() if 'across' in k}
        down_slots = {k: v for k, v in self.grid.slots.items() if 'down' in k}
        
        if across_slots:
            print("\n  ACROSS:")
            for slot_id in sorted(across_slots.keys(), key=lambda x: int(x.split('-')[0])):
                slot = across_slots[slot_id]
                pattern = slot.get_pattern(self.grid)
                print(f"    {slot.number}. {pattern} ({slot.length} letters)")
        
        if down_slots:
            print("\n  DOWN:")
            for slot_id in sorted(down_slots.keys(), key=lambda x: int(x.split('-')[0])):
                slot = down_slots[slot_id]
                pattern = slot.get_pattern(self.grid)
                print(f"    {slot.number}. {pattern} ({slot.length} letters)")
    
    def solve_puzzle(self, verbose: bool = True, max_attempts: int = 1000000) -> bool:
        """
        Solve the loaded puzzle.
        
        Args:
            verbose: Show progress during solving
            max_attempts: Maximum word placement attempts
            
        Returns:
            True if solved
        """
        if not self.grid:
            print("Error: No puzzle loaded. Use load_puzzle_from_file() or create_puzzle_interactive().")
            return False
        
        if not self.lexicon.all_words:
            print("Error: No dictionary loaded. Use load_dictionary().")
            return False
        
        print("\n" + "="*60)
        print("SOLVING PUZZLE")
        print("="*60)
        
        self.solver = CrosswordSolver(self.grid, self.lexicon)
        success = self.solver.solve(verbose=verbose, max_attempts=max_attempts)
        
        if success:
            self.solver.print_solution()
        
        return success
    
    def save_solution(self, filepath: str) -> bool:
        """
        Save the solved puzzle to a file.
        
        Args:
            filepath: Output file path
            
        Returns:
            True if successful
        """
        if not self.solver or not self.solver.solution:
            print("Error: No solution available.")
            return False
        
        try:
            with open(filepath, 'w') as f:
                f.write("="*60 + "\n")
                f.write("CROSSWORD SOLUTION\n")
                f.write("="*60 + "\n\n")
                
                # Write the filled grid
                f.write("Grid:\n")
                for row in self.grid.grid:
                    f.write(" ".join(row) + "\n")
                
                f.write("\n" + "="*60 + "\n")
                
                # Write solution list
                solution = self.solver.get_solution()
                across = {k: v for k, v in solution.items() if 'across' in k}
                down = {k: v for k, v in solution.items() if 'down' in k}
                
                if across:
                    f.write("\nACROSS:\n")
                    for slot_id in sorted(across.keys(), key=lambda x: int(x.split('-')[0])):
                        slot = self.grid.slots[slot_id]
                        f.write(f"  {slot.number}. {across[slot_id]} ({slot.length} letters)\n")
                
                if down:
                    f.write("\nDOWN:\n")
                    for slot_id in sorted(down.keys(), key=lambda x: int(x.split('-')[0])):
                        slot = self.grid.slots[slot_id]
                        f.write(f"  {slot.number}. {down[slot_id]} ({slot.length} letters)\n")
            
            print(f"\n✓ Solution saved to: {filepath}")
            return True
        except Exception as e:
            print(f"Error saving solution: {e}")
            return False
    
    def run_interactive(self) -> None:
        """
        Run the solver in interactive mode.
        """
        print("\n" + "="*60)
        print("🧩 CROSSWORD PUZZLE SOLVER 🧩")
        print("="*60)
        print("\nWelcome! This solver uses constraint satisfaction with")
        print("backtracking to fill crossword grids.")
        print()
        
        # Load dictionary
        print("📚 Loading dictionary...")
        self.load_dictionary()
        print()
        
        # Get puzzle
        while True:
            print("How would you like to input the puzzle?")
            print("  1. Load from file")
            print("  2. Enter manually")
            print("  3. Use example puzzle")
            
            try:
                choice = input("\nChoice (1-3): ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nGoodbye!")
                return
            
            if choice == "1":
                filepath = input("Enter puzzle file path: ").strip()
                if self.load_puzzle_from_file(filepath):
                    break
            elif choice == "2":
                if self.create_puzzle_interactive():
                    break
            elif choice == "3":
                self._load_example_puzzle()
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.\n")
        
        # Display puzzle
        self.display_puzzle()
        
        # Solve
        input("\nPress Enter to solve...")
        success = self.solve_puzzle()
        
        # Save option
        if success:
            try:
                save = input("\nSave solution to file? (y/n): ").strip().lower()
                if save == 'y':
                    filepath = input("Output file path: ").strip()
                    self.save_solution(filepath)
            except (EOFError, KeyboardInterrupt):
                pass
        
        print("\nThank you for using Crossword Puzzle Solver!")
    
    def _load_example_puzzle(self) -> None:
        """Load a built-in example puzzle."""
        print("\nLoading example 5x5 puzzle...")
        
        # Example 5x5 puzzle
        example = [
            ".....",
            ".#.#.",
            ".....",
            ".#.#.",
            "....."
        ]
        
        self.grid = Grid(example)
        print(f"✓ Loaded example: {self.grid.rows}x{self.grid.cols}")


# Command-line interface
def main():
    """Main entry point for the crossword solver."""
    interface = CrosswordInterface()
    interface.run_interactive()


if __name__ == "__main__":
    main()
