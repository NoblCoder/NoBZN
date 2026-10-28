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
    
    def __init__(self, grid: Grid, lexicon: Lexicon, candidates=None, allow_repeats=False):
        self.grid = grid
        self.lexicon = lexicon
        self.candidates = candidates or {}
        unknown = set(self.candidates) - set(grid.slots)
        if unknown:
            raise ValueError(f"Unknown slots: {sorted(unknown)}")
        self.allow_repeats = allow_repeats
        self.solution = {}
        self.filled_slots = set()
        self.attempts = self.backtracks = 0
        self.status = "not_started"

    def _domain(self, slot_id):
        pattern = self.grid.slots[slot_id].get_pattern(self.grid)
        words = self.candidates.get(slot_id)
        if words is None:
            words = self.lexicon.match_pattern(pattern)
        used = set(self.solution.values())
        return sorted({w.upper() for w in words
                       if len(w) == len(pattern) and w.isascii() and w.isalpha()
                       and all(p == '_' or p == c for p, c in zip(pattern, w.upper()))
                       and (self.allow_repeats or w.upper() not in used)})

    def solve(self, verbose=True, max_attempts=1000000):
        if max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        self.start_time = time.time()
        self.attempts = self.backtracks = 0
        self.solution = {}
        self.filled_slots = set()
        self.status = "searching"
        covered = {cell for slot in self.grid.slots.values() for cell in slot.cells}
        if not self.grid.slots or any(
            self.grid.get_cell(r, c) != '#' and (r, c) not in covered
            for r in range(self.grid.rows) for c in range(self.grid.cols)
        ):
            self.status = "invalid_grid"
            if verbose:
                print("Cannot solve: every white cell must belong to a word of at least two letters.")
            return False
        result = self._search(max_attempts)
        if result:
            self.status = "solved"
        elif self.status != "limit_reached":
            self.status = "no_solution"
        if verbose:
            print(f"{self.status}: {self.attempts} attempts, {self.backtracks} backtracks")
        return result

    def _search(self, limit):
        if len(self.solution) == len(self.grid.slots):
            return True
        domains = {sid: self._domain(sid) for sid in self.grid.slots if sid not in self.solution}
        sid = min(domains, key=lambda s: (len(domains[s]),
                  -len(self.grid.get_intersections_for_slot(s)), s))
        if not domains[sid]:
            return False
        slot = self.grid.slots[sid]
        saved = [self.grid.get_cell(r, c) for r, c in slot.cells]
        for word in domains[sid]:
            if self.attempts >= limit:
                self.status = "limit_reached"
                return False
            self.attempts += 1
            self.grid.fill_slot(sid, word)
            self.solution[sid] = word
            self.filled_slots.add(sid)
            if self._search(limit):
                return True
            for (r, c), char in zip(slot.cells, saved):
                self.grid.set_cell(r, c, char)
            del self.solution[sid]
            self.filled_slots.remove(sid)
            self.backtracks += 1
            if self.status == "limit_reached":
                return False
        return False

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
