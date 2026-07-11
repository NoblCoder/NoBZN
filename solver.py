"""
🟢 CONSTRAINT SOLVER MODULE (The Algorithm)
The engine room - implements backtracking with constraint propagation.
"""

from typing import List, Dict, Set, Optional, Tuple
import time
from grid import Grid, Slot
from lexicon import Lexicon


class CrosswordSolver:
    """
    Solves crossword puzzles using constraint satisfaction with backtracking.
    """
    
    def __init__(self, grid: Grid, lexicon: Lexicon):
        """
        Initialize the solver.
        
        Args:
            grid: The Grid object representing the puzzle
            lexicon: The Lexicon object with the word dictionary
        """
        self.grid = grid
        self.lexicon = lexicon
        
        # Tracking
        self.attempts = 0
        self.backtracks = 0
        self.start_time = 0
        
        # Solution state
        self.solution: Dict[str, str] = {}  # slot_id -> word
        self.filled_slots: Set[str] = set()
    
    def solve(self, verbose: bool = True, max_attempts: int = 1000000) -> bool:
        """
        Solve the crossword puzzle.
        
        Args:
            verbose: If True, print progress updates
            max_attempts: Maximum number of word placement attempts
            
        Returns:
            True if solved, False if no solution found
        """
        self.start_time = time.time()
        self.attempts = 0
        self.backtracks = 0
        self.solution = {}
        self.filled_slots = set()
        
        if verbose:
            print("🔍 Starting crossword solver...")
            print(f"   Grid: {self.grid.rows}x{self.grid.cols}")
            print(f"   Slots: {len(self.grid.slots)}")
            print(f"   Intersections: {len(self.grid.intersections)}")
            print()
        
        # Get ordered list of slots using MRV heuristic
        slot_order = self._get_slot_order()
        
        # Start backtracking
        result = self._backtrack(slot_order, 0, verbose, max_attempts)
        
        elapsed = time.time() - self.start_time
        
        if verbose:
            print()
            if result:
                print(f"✅ SOLVED in {elapsed:.2f}s!")
            else:
                print(f"❌ No solution found after {elapsed:.2f}s")
            print(f"   Attempts: {self.attempts:,}")
            print(f"   Backtracks: {self.backtracks:,}")
        
        return result
    
    def _get_slot_order(self) -> List[str]:
        """
        Order slots using heuristics for efficient solving.
        
        Uses the Minimum Remaining Values (MRV) heuristic:
        - Prioritize slots with fewer possible words
        - Break ties by number of intersections (more = higher priority)
        """
        slot_scores = []
        
        for slot_id, slot in self.grid.slots.items():
            # Count possible words for this slot
            pattern = slot.get_pattern(self.grid)
            possible_words = self.lexicon.match_pattern(pattern)
            num_candidates = len(possible_words)
            
            # Count intersections
            intersections = self.grid.get_intersections_for_slot(slot_id)
            num_intersections = len(intersections)
            
            # Score: prioritize fewer candidates, then more intersections
            # Use negative for sorting (lower is better)
            score = (num_candidates, -num_intersections, slot_id)
            slot_scores.append((score, slot_id))
        
        # Sort by score
        slot_scores.sort()
        return [slot_id for _, slot_id in slot_scores]
    
    def _backtrack(self, slot_order: List[str], index: int, verbose: bool, max_attempts: int) -> bool:
        """
        Recursive backtracking algorithm.
        
        Args:
            slot_order: Ordered list of slot IDs to fill
            index: Current index in slot_order
            verbose: Whether to print progress
            max_attempts: Maximum attempts before giving up
            
        Returns:
            True if solution found, False otherwise
        """
        # Check attempt limit
        if self.attempts >= max_attempts:
            if verbose:
                print(f"\n⚠️  Reached maximum attempts ({max_attempts:,})")
            return False
        
        # Base case: all slots filled
        if index >= len(slot_order):
            return True
        
        slot_id = slot_order[index]
        slot = self.grid.slots[slot_id]
        
        # Get current pattern and possible words
        pattern = slot.get_pattern(self.grid)
        candidates = self.lexicon.match_pattern(pattern)
        
        if verbose and self.attempts % 1000 == 0:
            progress = (index / len(slot_order)) * 100
            print(f"   Progress: {progress:.1f}% | Attempts: {self.attempts:,} | "
                  f"Backtracks: {self.backtracks:,} | Current: {slot_id}", end='\r')
        
        # If no candidates, backtrack immediately
        if not candidates:
            self.backtracks += 1
            return False
        
        # Try each candidate word
        for word in candidates:
            self.attempts += 1
            
            # Save current grid state (for backtracking)
            saved_state = self._save_slot_state(slot_id)
            
            # Place the word
            self.grid.fill_slot(slot_id, word)
            self.solution[slot_id] = word
            self.filled_slots.add(slot_id)
            
            # Check if this placement is consistent with constraints
            if self._is_consistent(slot_id):
                # Recurse to next slot
                if self._backtrack(slot_order, index + 1, verbose, max_attempts):
                    return True  # Solution found!
            
            # If we reach here, this word didn't work - backtrack
            self._restore_slot_state(slot_id, saved_state)
            self.solution.pop(slot_id, None)
            self.filled_slots.discard(slot_id)
            self.backtracks += 1
        
        # No word worked for this slot
        return False
    
    def _is_consistent(self, slot_id: str) -> bool:
        """
        Check if the current grid state is consistent after filling a slot.
        
        Verifies that all intersecting slots still have at least one
        possible word that could fit.
        
        Args:
            slot_id: The slot that was just filled
            
        Returns:
            True if consistent (no dead ends), False otherwise
        """
        intersections = self.grid.get_intersections_for_slot(slot_id)
        
        for inter in intersections:
            # Get the other slot involved in this intersection
            other_slot_id = inter.slot2 if inter.slot1 == slot_id else inter.slot1
            
            # Skip if already filled
            if other_slot_id in self.filled_slots:
                continue
            
            # Check if the other slot still has valid candidates
            other_slot = self.grid.slots[other_slot_id]
            pattern = other_slot.get_pattern(self.grid)
            candidates = self.lexicon.match_pattern(pattern)
            
            # Dead end: no words can fit this pattern
            if not candidates:
                return False
        
        return True
    
    def _save_slot_state(self, slot_id: str) -> List[str]:
        """Save the current state of a slot's cells."""
        slot = self.grid.slots[slot_id]
        return [self.grid.get_cell(r, c) for r, c in slot.cells]
    
    def _restore_slot_state(self, slot_id: str, state: List[str]) -> None:
        """Restore a slot's cells to a saved state."""
        slot = self.grid.slots[slot_id]
        for i, (r, c) in enumerate(slot.cells):
            self.grid.set_cell(r, c, state[i])
    
    def get_solution(self) -> Dict[str, str]:
        """
        Get the solution as a dictionary of slot_id -> word.
        
        Returns:
            Dictionary mapping slot IDs to words
        """
        return self.solution.copy()
    
    def print_solution(self) -> None:
        """Print the solution in a readable format."""
        if not self.solution:
            print("No solution available.")
            return
        
        print("\n" + "="*50)
        print("SOLUTION")
        print("="*50)
        
        # Group by across/down
        across = {k: v for k, v in self.solution.items() if 'across' in k}
        down = {k: v for k, v in self.solution.items() if 'down' in k}
        
        if across:
            print("\nACROSS:")
            for slot_id in sorted(across.keys(), key=lambda x: int(x.split('-')[0])):
                slot = self.grid.slots[slot_id]
                print(f"  {slot.number}. {across[slot_id]} ({slot.length} letters)")
        
        if down:
            print("\nDOWN:")
            for slot_id in sorted(down.keys(), key=lambda x: int(x.split('-')[0])):
                slot = self.grid.slots[slot_id]
                print(f"  {slot.number}. {down[slot_id]} ({slot.length} letters)")
        
        print("\n" + "="*50)
        print("\nFilled Grid:")
        print(self.grid)


# Test function
def test_solver():
    """Test the solver with a simple puzzle."""
    print("=== Constraint Solver Test ===\n")
    
    # Create a simple 3x3 puzzle
    test_grid = [
        "...",
        ".#.",
        "..."
    ]
    
    from grid import Grid
    from lexicon import Lexicon
    
    grid = Grid(test_grid)
    lexicon = Lexicon()
    lexicon._load_minimal_words()
    
    print("Initial Grid:")
    print(grid)
    print()
    
    solver = CrosswordSolver(grid, lexicon)
    success = solver.solve(verbose=True)
    
    if success:
        solver.print_solution()


if __name__ == "__main__":
    test_solver()
