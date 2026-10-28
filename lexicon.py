"""
🟠 LEXICON MODULE (Data Layer)
The solver's brain - handles dictionary loading, word organization, and pattern matching.
"""

import re
from collections import defaultdict
from typing import Dict, List, Set


class Lexicon:
    """
    Manages the word dictionary with fast lookups by length and pattern matching.
    """
    
    def __init__(self):
        self.words_by_length: Dict[int, Set[str]] = defaultdict(set)
        self.all_words: Set[str] = set()
    
    def load_from_file(self, filepath: str) -> None:
        """
        Load words from a dictionary file and organize by length.
        
        Args:
            filepath: Path to a text file with one word per line
        """
        print(f"Loading dictionary from {filepath}...")
        word_count = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().upper()
                if re.fullmatch(r"[A-Z]+", word):
                    self.all_words.add(word)
                    self.words_by_length[len(word)].add(word)
                    word_count += 1
        if not word_count:
            raise ValueError("Dictionary contains no A-Z words")
        print(f"✓ Loaded {word_count} words")

    def _load_system_words(self) -> None:
        """Load a system dictionary, or a small portable demonstration list."""
        from pathlib import Path
        for path in ('/usr/share/dict/words', '/usr/dict/words'):
            if Path(path).is_file():
                self.load_from_file(path)
                return
        print("No system dictionary found; using demonstration vocabulary. "
              "Supply -d for larger fill-in puzzles or JSON candidates for a crossword.")
        self._load_minimal_words()

    def _load_minimal_words(self) -> None:
        """
        Minimal fallback word list for testing.
        """
        minimal_words = [
            "CAR", "TEN", "CAN", "RAN", "AS", "AT", "BE", "BY", "DO", "GO", "HE", "IF", "IN", "IS", "IT", "ME", "MY", "NO", "OF", "ON", "OR", "SO", "TO", "UP", "US", "WE", "CAT", "DOG", "BAT", "RAT", "HAT", "MAT", "SAT", "FAT",
            "CATS", "DOGS", "BATS", "RATS", "HATS", "MATS", "FATS",
            "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL",
            "CAN", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET",
            "BAKER", "BIKES", "TAKEN", "MAKES", "LAKES", "CAKES",
        ]
        
        for word in minimal_words:
            word = word.upper()
            self.all_words.add(word)
            self.words_by_length[len(word)].add(word)
        
        print(f"✓ Loaded {len(minimal_words)} minimal words")
    
    def get_words_by_length(self, length: int) -> Set[str]:
        """
        Get all words of a specific length.
        
        Args:
            length: Number of letters
            
        Returns:
            Set of words with the specified length
        """
        return self.words_by_length.get(length, set())
    
    def match_pattern(self, pattern: str) -> List[str]:
        """
        Find all words matching a pattern with wildcards.
        
        Pattern rules:
            - Letters (A-Z) must match exactly
            - Underscore (_) or period (.) matches any letter
            - Pattern is case-insensitive
        
        Examples:
            "B_KE_" matches BAKER, BIKES, BIKER, etc.
            "C.T" matches CAT, COT, CUT, etc.
        
        Args:
            pattern: String with letters and wildcards (_/.)
            
        Returns:
            List of matching words, sorted alphabetically
        """
        pattern = pattern.upper()
        if not re.fullmatch(r"[A-Z_.]+", pattern):
            return []
        length = len(pattern)
        
        # Convert pattern to regex: _ or . becomes [A-Z]
        regex_pattern = pattern.replace('_', '[A-Z]').replace('.', '[A-Z]')
        regex_pattern = f"^{regex_pattern}$"
        
        try:
            compiled_pattern = re.compile(regex_pattern)
        except re.error:
            return []
        
        # Only search words of the correct length
        candidates = self.words_by_length.get(length, set())
        matches = [word for word in candidates if compiled_pattern.match(word)]
        
        return sorted(matches)
    
    def is_valid_word(self, word: str) -> bool:
        """
        Check if a word exists in the dictionary.
        
        Args:
            word: Word to check
            
        Returns:
            True if word is in dictionary
        """
        return word.upper() in self.all_words
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the loaded dictionary.
        
        Returns:
            Dictionary with stats
        """
        if not self.words_by_length:
            return {"total_words": 0, "lengths": {}}
        
        return {
            "total_words": len(self.all_words),
            "min_length": min(self.words_by_length.keys()),
            "max_length": max(self.words_by_length.keys()),
            "lengths": {
                length: len(words) 
                for length, words in sorted(self.words_by_length.items())
            }
        }


# Quick test function
def test_lexicon():
    """Test the lexicon with some basic patterns."""
    lex = Lexicon()
    lex._load_minimal_words()
    
    print("\n=== Lexicon Test ===")
    print(f"Total words: {len(lex.all_words)}")
    
    print("\n5-letter words:", sorted(lex.get_words_by_length(5))[:10])
    
    print("\nPattern 'B_KE_' matches:", lex.match_pattern("B_KE_"))
    print("Pattern 'C_T' matches:", lex.match_pattern("C_T"))
    print("Pattern '___' matches:", lex.match_pattern("___")[:10])
    
    print("\nIs 'CAT' valid?", lex.is_valid_word("cat"))
    print("Is 'XYZ' valid?", lex.is_valid_word("xyz"))


if __name__ == "__main__":
    test_lexicon()
