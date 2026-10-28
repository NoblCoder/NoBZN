import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from grid import Grid
from lexicon import Lexicon
from solver import CrosswordSolver
from interface import CrosswordInterface


class RegressionTests(unittest.TestCase):
    def test_slot_starts(self):
        grid = Grid(['...', '...', '...'])
        self.assertEqual(len(grid.slots), 6)
        self.assertEqual(sum(s.direction.value == 'across' for s in grid.slots.values()), 3)

    def test_bad_grids(self):
        for rows in ([], [''], ['..', '.'], ['?']):
            with self.assertRaises(ValueError):
                Grid(rows)

    def test_black_rows_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / 'grid.txt'
            p.write_text('# prose comment\n#..\n###\n..#\n')
            app = CrosswordInterface()
            self.assertTrue(app.load_puzzle_from_file(str(p)))
            self.assertEqual(app.grid.rows, 3)
            self.assertEqual(app.grid.grid[1], list('###'))

    def test_clued_solution(self):
        app = CrosswordInterface()
        self.assertTrue(app.load_puzzle_from_file('example_puzzles/clued_3x3.json'))
        solver = CrosswordSolver(app.grid, app.lexicon, app.candidates)
        self.assertTrue(solver.solve(False))
        self.assertEqual(solver.solution, {'1-across': 'CAT', '1-down': 'CAR', '2-down': 'TEN', '3-across': 'RAN'})
        self.assertEqual([''.join(r) for r in app.grid.grid], ['CAT', 'A#E', 'RAN'])

    def test_limit_restores_grid_and_is_exact(self):
        g = Grid(['...', '.#.', '...'])
        lex = Lexicon()
        lex._load_minimal_words()
        original = [row[:] for row in g.grid]
        solver = CrosswordSolver(g, lex)
        self.assertFalse(solver.solve(False, 1))
        self.assertEqual(solver.status, 'limit_reached')
        self.assertEqual(solver.attempts, 1)
        self.assertEqual(g.grid, original)
        self.assertEqual(solver.solution, {})

    def test_no_duplicate_answers(self):
        g = Grid(['CAT#CAT'])
        lex = Lexicon()
        lex._load_minimal_words()
        self.assertFalse(CrosswordSolver(g, lex).solve(False))
        self.assertTrue(CrosswordSolver(g, lex, allow_repeats=True).solve(False, 2))

    def test_uncovered_cells(self):
        self.assertFalse(CrosswordSolver(Grid(['.#.']), Lexicon()).solve(False))

    def test_missing_dictionary_does_not_recurse(self):
        lex = Lexicon()
        with patch('pathlib.Path.is_file', return_value=False):
            lex._load_system_words()
        self.assertTrue(lex.is_valid_word('CAT'))
        with self.assertRaises(FileNotFoundError):
            lex.load_from_file('/nonexistent/words.txt')

    def test_pattern_cannot_inject_regex(self):
        lex = Lexicon()
        lex._load_minimal_words()
        self.assertEqual(lex.match_pattern('C|T'), [])

    def test_unknown_clue_is_not_guessed(self):
        from clues import clue_candidates
        with self.assertRaisesRegex(ValueError, 'No offline answers'):
            clue_candidates(Grid(['...']), {'1-across': 'unknown clue'}, {})


if __name__ == '__main__':
    unittest.main()
