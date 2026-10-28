"""
🔵 GRID ENGINE MODULE (State Management)
Handles the physical layout of the puzzle - spaces, coordinates, slots, and intersections.
"""

from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """Direction of a word slot in the grid."""
    ACROSS = "across"
    DOWN = "down"


@dataclass
class Slot:
    """
    Represents a word slot in the crossword grid.
    
    Attributes:
        number: Clue number (1, 2, 3, etc.)
        direction: ACROSS or DOWN
        row: Starting row (0-indexed)
        col: Starting column (0-indexed)
        length: Number of letters
        cells: List of (row, col) tuples for each letter position
    """
    number: int
    direction: Direction
    row: int
    col: int
    length: int
    cells: List[Tuple[int, int]]
    
    def __repr__(self):
        return f"{self.number}-{self.direction.value.capitalize()} ({self.length} letters)"
    
    def get_pattern(self, grid: 'Grid') -> str:
        """
        Get the current pattern for this slot from the grid.
        Returns a string with letters and underscores for empty cells.
        """
        return ''.join(grid.get_cell(row, col) for row, col in self.cells)


@dataclass
class Intersection:
    """
    Represents where two slots cross.
    
    Attributes:
        slot1: First slot ID (e.g., "1-across")
        slot2: Second slot ID (e.g., "2-down")
        position1: Letter index in slot1 (0-indexed)
        position2: Letter index in slot2 (0-indexed)
        cell: The (row, col) where they intersect
    """
    slot1: str
    slot2: str
    position1: int
    position2: int
    cell: Tuple[int, int]
    
    def __repr__(self):
        return f"{self.slot1}[{self.position1}] ↔ {self.slot2}[{self.position2}] @ {self.cell}"


class Grid:
    """
    Manages the crossword grid state and coordinates.
    
    Grid representation:
        - '.' or '_' = empty cell (white square)
        - '#' = blocked cell (black square)
        - 'A'-'Z' = filled letter
    """
    
    def __init__(self, grid_data: List[str]):
        """
        Initialize grid from a list of strings.
        
        Args:
            grid_data: List of strings, each representing a row.
                      Use '.' or '_' for empty, '#' for blocked.
        """
        if not grid_data or not grid_data[0]:
            raise ValueError("Grid must contain nonempty rows")
        if any(len(row) != len(grid_data[0]) for row in grid_data):
            raise ValueError("Grid rows must have equal widths")
        if any(c not in "._#ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" for row in grid_data for c in row):
            raise ValueError("Grid accepts only A-Z, '.', '_' and '#'")
        self.grid = [list(row.upper()) for row in grid_data]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0
        
        # Normalize empty cells to underscore
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == '.':
                    self.grid[r][c] = '_'
        
        # Extract slots and intersections
        self.slots: Dict[str, Slot] = {}
        self.intersections: List[Intersection] = []
        self._extract_slots()
        self._calculate_intersections()
    
    def get_cell(self, row: int, col: int) -> str:
        """Get the character at a specific cell."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return '#'  # Out of bounds = blocked
    
    def set_cell(self, row: int, col: int, char: str) -> None:
        """Set a character at a specific cell."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = char.upper()
    
    def is_blocked(self, row: int, col: int) -> bool:
        """Check if a cell is blocked."""
        return self.get_cell(row, col) == '#'
    
    def is_empty(self, row: int, col: int) -> bool:
        """Check if a cell is empty (underscore)."""
        return self.get_cell(row, col) == '_'
    
    def _extract_slots(self) -> None:
        """
        Scan the grid to find all word slots (across and down).
        """
        slot_number = 1
        numbered_cells = {}  # (row, col) -> number
        
        # First pass: number the cells that start a word
        for r in range(self.rows):
            for c in range(self.cols):
                if self.is_blocked(r, c):
                    continue
                
                # Check if this cell starts an across word
                starts_across = (
                    (c == 0 or self.is_blocked(r, c - 1)) and
                    c + 1 < self.cols and not self.is_blocked(r, c + 1)
                )
                
                # Check if this cell starts a down word
                starts_down = (
                    (r == 0 or self.is_blocked(r - 1, c)) and
                    r + 1 < self.rows and not self.is_blocked(r + 1, c)
                )
                
                if starts_across or starts_down:
                    numbered_cells[(r, c)] = slot_number
                    slot_number += 1
        
        # Second pass: extract the actual slots
        for (r, c), num in numbered_cells.items():
            # Extract across slot
            if (c == 0 or self.is_blocked(r, c - 1)) and c + 1 < self.cols and not self.is_blocked(r, c + 1):
                cells = []
                col = c
                while col < self.cols and not self.is_blocked(r, col):
                    cells.append((r, col))
                    col += 1
                
                if len(cells) > 1:  # Only add if it's at least 2 letters
                    slot_id = f"{num}-across"
                    self.slots[slot_id] = Slot(
                        number=num,
                        direction=Direction.ACROSS,
                        row=r,
                        col=c,
                        length=len(cells),
                        cells=cells
                    )
            
            # Extract down slot
            if (r == 0 or self.is_blocked(r - 1, c)) and r + 1 < self.rows and not self.is_blocked(r + 1, c):
                cells = []
                row = r
                while row < self.rows and not self.is_blocked(row, c):
                    cells.append((row, c))
                    row += 1
                
                if len(cells) > 1:  # Only add if it's at least 2 letters
                    slot_id = f"{num}-down"
                    self.slots[slot_id] = Slot(
                        number=num,
                        direction=Direction.DOWN,
                        row=r,
                        col=c,
                        length=len(cells),
                        cells=cells
                    )
    
    def _calculate_intersections(self) -> None:
        """
        Calculate all intersection points between slots.
        This is crucial for the constraint solver.
        """
        slot_items = list(self.slots.items())
        
        for i, (id1, slot1) in enumerate(slot_items):
            for id2, slot2 in slot_items[i + 1:]:
                # Skip if both slots go in the same direction
                if slot1.direction == slot2.direction:
                    continue
                
                # Find intersecting cells
                cells1_set = set(slot1.cells)
                cells2_set = set(slot2.cells)
                common_cells = cells1_set & cells2_set
                
                for cell in common_cells:
                    pos1 = slot1.cells.index(cell)
                    pos2 = slot2.cells.index(cell)
                    
                    self.intersections.append(Intersection(
                        slot1=id1,
                        slot2=id2,
                        position1=pos1,
                        position2=pos2,
                        cell=cell
                    ))
    
    def fill_slot(self, slot_id: str, word: str) -> bool:
        """
        Fill a slot with a word.
        
        Args:
            slot_id: The slot identifier (e.g., "1-across")
            word: The word to fill
            
        Returns:
            True if successful, False if word length doesn't match
        """
        slot = self.slots.get(slot_id)
        if not slot:
            return False
        
        word = word.upper()
        if len(word) != slot.length:
            return False
        
        for i, (row, col) in enumerate(slot.cells):
            self.set_cell(row, col, word[i])
        
        return True
    
    def clear_slot(self, slot_id: str) -> None:
        """Clear a slot (set all cells to underscore)."""
        slot = self.slots.get(slot_id)
        if slot:
            for row, col in slot.cells:
                self.set_cell(row, col, '_')
    
    def get_intersections_for_slot(self, slot_id: str) -> List[Intersection]:
        """Get all intersections involving a specific slot."""
        return [
            inter for inter in self.intersections
            if inter.slot1 == slot_id or inter.slot2 == slot_id
        ]
    
    def display(self) -> str:
        """
        Generate a string representation of the grid.
        """
        lines = []
        lines.append("┌" + "─" * (self.cols * 2 + 1) + "┐")
        
        for row in self.grid:
            line = "│ " + " ".join(row) + " │"
            lines.append(line)
        
        lines.append("└" + "─" * (self.cols * 2 + 1) + "┘")
        return "\n".join(lines)
    
    def __str__(self):
        return self.display()


# Test function
def test_grid():
    """Test the grid with a simple 3x3 puzzle."""
    print("=== Grid Engine Test ===\n")
    
    # Simple 3x3 grid
    test_grid = [
        "...",
        ".#.",
        "..."
    ]
    
    grid = Grid(test_grid)
    
    print("Initial Grid:")
    print(grid)
    
    print(f"\nGrid dimensions: {grid.rows}x{grid.cols}")
    print(f"Total slots: {len(grid.slots)}")
    
    print("\nSlots:")
    for slot_id, slot in grid.slots.items():
        print(f"  {slot_id}: {slot}")
    
    print(f"\nIntersections: {len(grid.intersections)}")
    for inter in grid.intersections:
        print(f"  {inter}")
    
    print("\nFilling 1-across with 'CAT':")
    grid.fill_slot("1-across", "CAT")
    print(grid)
    
    print("\nPattern for 2-down:", grid.slots["2-down"].get_pattern(grid))


if __name__ == "__main__":
    test_grid()
