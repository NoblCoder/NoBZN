"""
⚡ OPTIMIZATIONS & ADVANCED FEATURES

Additional enhancements for the crossword solver including:
- Performance profiling
- Advanced heuristics
- Arc consistency checks
- Word frequency scoring
"""

from typing import Dict, List, Set, Tuple, Optional
from collections import Counter
import time


class PerformanceProfiler:
    """
    Tracks detailed performance metrics during solving.
    """
    
    def __init__(self):
        self.start_time = 0
        self.metrics = {
            'total_attempts': 0,
            'successful_placements': 0,
            'failed_placements': 0,
            'backtracks': 0,
            'constraint_checks': 0,
            'pattern_matches': 0,
            'slot_times': {},  # slot_id -> time spent
        }
        self.slot_start_time = None
        self.current_slot = None
    
    def start(self):
        """Start the profiler."""
        self.start_time = time.time()
        self.metrics = {
            'total_attempts': 0,
            'successful_placements': 0,
            'failed_placements': 0,
            'backtracks': 0,
            'constraint_checks': 0,
            'pattern_matches': 0,
            'slot_times': {},
        }
    
    def start_slot(self, slot_id: str):
        """Mark the start of working on a slot."""
        self.current_slot = slot_id
        self.slot_start_time = time.time()
    
    def end_slot(self, slot_id: str, success: bool):
        """Mark the end of working on a slot."""
        if self.slot_start_time and self.current_slot == slot_id:
            elapsed = time.time() - self.slot_start_time
            if slot_id not in self.metrics['slot_times']:
                self.metrics['slot_times'][slot_id] = 0
            self.metrics['slot_times'][slot_id] += elapsed
            
            if success:
                self.metrics['successful_placements'] += 1
            else:
                self.metrics['failed_placements'] += 1
    
    def record_attempt(self):
        """Record a word placement attempt."""
        self.metrics['total_attempts'] += 1
    
    def record_backtrack(self):
        """Record a backtrack."""
        self.metrics['backtracks'] += 1
    
    def record_constraint_check(self):
        """Record a constraint consistency check."""
        self.metrics['constraint_checks'] += 1
    
    def record_pattern_match(self):
        """Record a pattern matching operation."""
        self.metrics['pattern_matches'] += 1
    
    def get_report(self) -> str:
        """Generate a performance report."""
        elapsed = time.time() - self.start_time
        
        report = [
            "\n" + "="*60,
            "PERFORMANCE REPORT",
            "="*60,
            f"Total Time: {elapsed:.3f}s",
            f"Total Attempts: {self.metrics['total_attempts']:,}",
            f"Successful Placements: {self.metrics['successful_placements']:,}",
            f"Failed Placements: {self.metrics['failed_placements']:,}",
            f"Backtracks: {self.metrics['backtracks']:,}",
            f"Constraint Checks: {self.metrics['constraint_checks']:,}",
            f"Pattern Matches: {self.metrics['pattern_matches']:,}",
        ]
        
        if self.metrics['total_attempts'] > 0:
            attempts_per_sec = self.metrics['total_attempts'] / elapsed
            report.append(f"Attempts/Second: {attempts_per_sec:,.0f}")
        
        # Top slowest slots
        if self.metrics['slot_times']:
            report.append("\nSlowest Slots:")
            sorted_slots = sorted(
                self.metrics['slot_times'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            for slot_id, slot_time in sorted_slots:
                report.append(f"  {slot_id}: {slot_time:.3f}s")
        
        report.append("="*60)
        return "\n".join(report)


class WordFrequencyScorer:
    """
    Scores words based on letter frequency to prefer common words.
    This can help the solver find solutions faster.
    """
    
    # Letter frequency in English (based on typical usage)
    LETTER_FREQ = {
        'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
        'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
        'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
        'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
        'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
        'Z': 0.07
    }
    
    @classmethod
    def score_word(cls, word: str) -> float:
        """
        Score a word based on letter frequencies.
        Higher score = more common letters.
        
        Args:
            word: The word to score
            
        Returns:
            Score (0-100)
        """
        if not word:
            return 0.0
        
        total = sum(cls.LETTER_FREQ.get(letter.upper(), 0.5) for letter in word)
        return total / len(word)
    
    @classmethod
    def sort_by_frequency(cls, words: List[str]) -> List[str]:
        """
        Sort words by frequency score (highest first).
        
        Args:
            words: List of words to sort
            
        Returns:
            Sorted list
        """
        return sorted(words, key=cls.score_word, reverse=True)


class AdvancedHeuristics:
    """
    Additional heuristics for smarter solving.
    """
    
    @staticmethod
    def degree_heuristic(slot_id: str, grid, filled_slots: Set[str]) -> int:
        """
        Count how many unfilled slots intersect with this slot.
        Higher degree = more constraints = should be filled earlier.
        
        Args:
            slot_id: The slot to check
            grid: The Grid object
            filled_slots: Set of already-filled slot IDs
            
        Returns:
            Number of unfilled intersecting slots
        """
        intersections = grid.get_intersections_for_slot(slot_id)
        degree = 0
        
        for inter in intersections:
            other_slot = inter.slot2 if inter.slot1 == slot_id else inter.slot1
            if other_slot not in filled_slots:
                degree += 1
        
        return degree
    
    @staticmethod
    def combined_heuristic(
        slot_id: str,
        grid,
        lexicon,
        filled_slots: Set[str]
    ) -> Tuple[int, int, int]:
        """
        Combine multiple heuristics for optimal slot ordering.
        
        Returns tuple for sorting:
        1. Number of candidates (MRV - fewer is better)
        2. Negative degree (more constrained is better)
        3. Slot ID (for consistency)
        
        Args:
            slot_id: The slot to evaluate
            grid: The Grid object
            lexicon: The Lexicon object
            filled_slots: Set of already-filled slots
            
        Returns:
            Tuple for sorting (lower is better)
        """
        slot = grid.slots[slot_id]
        pattern = slot.get_pattern(grid)
        candidates = lexicon.match_pattern(pattern)
        num_candidates = len(candidates)
        
        degree = AdvancedHeuristics.degree_heuristic(slot_id, grid, filled_slots)
        
        # Return tuple: (MRV, -degree, slot_id)
        # This prioritizes:
        # 1. Slots with fewer candidates (MRV)
        # 2. Slots with more unfilled intersections (degree)
        # 3. Consistent ordering by slot_id
        return (num_candidates, -degree, slot_id)


def analyze_puzzle_difficulty(grid, lexicon) -> Dict:
    """
    Analyze a puzzle to estimate its difficulty.
    
    Args:
        grid: The Grid object
        lexicon: The Lexicon object
        
    Returns:
        Dictionary with difficulty metrics
    """
    metrics = {
        'grid_size': grid.rows * grid.cols,
        'total_slots': len(grid.slots),
        'total_intersections': len(grid.intersections),
        'avg_slot_length': 0,
        'min_candidates': float('inf'),
        'max_candidates': 0,
        'avg_candidates': 0,
        'difficulty_score': 0,
    }
    
    slot_lengths = []
    candidate_counts = []
    
    for slot in grid.slots.values():
        slot_lengths.append(slot.length)
        pattern = slot.get_pattern(grid)
        candidates = lexicon.match_pattern(pattern)
        num_candidates = len(candidates)
        candidate_counts.append(num_candidates)
        
        metrics['min_candidates'] = min(metrics['min_candidates'], num_candidates)
        metrics['max_candidates'] = max(metrics['max_candidates'], num_candidates)
    
    if slot_lengths:
        metrics['avg_slot_length'] = sum(slot_lengths) / len(slot_lengths)
    
    if candidate_counts:
        metrics['avg_candidates'] = sum(candidate_counts) / len(candidate_counts)
    
    # Simple difficulty score:
    # Higher = harder
    # Based on: number of slots, average candidates, grid density
    density = len(grid.slots) / (grid.rows * grid.cols)
    metrics['difficulty_score'] = (
        len(grid.slots) * 10 +
        metrics['avg_candidates'] / 10 +
        (1 - density) * 100
    )
    
    return metrics


def print_difficulty_analysis(metrics: Dict):
    """Pretty-print difficulty analysis."""
    print("\n" + "="*60)
    print("PUZZLE DIFFICULTY ANALYSIS")
    print("="*60)
    print(f"Grid Size: {metrics['grid_size']} cells")
    print(f"Total Slots: {metrics['total_slots']}")
    print(f"Total Intersections: {metrics['total_intersections']}")
    print(f"Average Slot Length: {metrics['avg_slot_length']:.1f} letters")
    print(f"Candidate Range: {metrics['min_candidates']} - {metrics['max_candidates']:,}")
    print(f"Average Candidates per Slot: {metrics['avg_candidates']:,.0f}")
    print(f"\nDifficulty Score: {metrics['difficulty_score']:.1f}")
    
    # Interpret difficulty
    score = metrics['difficulty_score']
    if score < 100:
        level = "EASY 😊"
    elif score < 300:
        level = "MEDIUM 🤔"
    elif score < 600:
        level = "HARD 😰"
    else:
        level = "EXPERT 💀"
    
    print(f"Estimated Difficulty: {level}")
    print("="*60)


# Example usage
if __name__ == "__main__":
    from grid import Grid
    from lexicon import Lexicon
    
    # Test with a 5x5 puzzle
    test_grid = [
        ".....",
        ".#.#.",
        ".....",
        ".#.#.",
        "....."
    ]
    
    grid = Grid(test_grid)
    lexicon = Lexicon()
    lexicon._load_system_words()
    
    print("Testing Advanced Features...")
    
    # Analyze difficulty
    metrics = analyze_puzzle_difficulty(grid, lexicon)
    print_difficulty_analysis(metrics)
    
    # Test word frequency scoring
    print("\nWord Frequency Scoring:")
    test_words = ["XYLOPHONE", "HELLO", "WORLD", "ZEBRA", "QUIET"]
    for word in test_words:
        score = WordFrequencyScorer.score_word(word)
        print(f"  {word}: {score:.2f}")
    
    print("\nSorted by frequency:")
    sorted_words = WordFrequencyScorer.sort_by_frequency(test_words)
    print(f"  {', '.join(sorted_words)}")
