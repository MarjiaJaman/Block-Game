"""Tests for tetris.py — validates game logic and that removed UI elements stay removed."""

import inspect
import sys
import types
import unittest

# ---------------------------------------------------------------------------
# Stub out pygame before importing tetris so tests can run without a display.
# ---------------------------------------------------------------------------
_pygame_stub = types.ModuleType('pygame')

# Minimal constants / classes used at module level in tetris.py
_pygame_stub.K_LEFT = 1
_pygame_stub.K_RIGHT = 2
_pygame_stub.K_UP = 3
_pygame_stub.K_SPACE = 4
_pygame_stub.K_m = 5
_pygame_stub.QUIT = 256
_pygame_stub.KEYDOWN = 768

sys.modules.setdefault('pygame', _pygame_stub)

import tetris  # noqa: E402  (import after stub)


class TestRotate(unittest.TestCase):
    def test_rotate_square(self):
        shape = [[1, 0], [0, 1]]
        rotated = tetris.rotate(shape)
        self.assertEqual(rotated, [[0, 1], [1, 0]])

    def test_rotate_i_piece(self):
        shape = [[1, 1, 1, 1]]
        rotated = tetris.rotate(shape)
        self.assertEqual(rotated, [[1], [1], [1], [1]])


class TestTetrisInit(unittest.TestCase):
    def setUp(self):
        self.game = tetris.Tetris()

    def test_initial_score(self):
        self.assertEqual(self.game.score, 0)

    def test_initial_lines(self):
        self.assertEqual(self.game.lines, 0)

    def test_initial_level(self):
        self.assertEqual(self.game.level, 1)

    def test_grid_dimensions(self):
        self.assertEqual(len(self.game.grid), tetris.ROWS)
        for row in self.game.grid:
            self.assertEqual(len(row), tetris.COLUMNS)

    def test_grid_initially_empty(self):
        for row in self.game.grid:
            for cell in row:
                self.assertIsNone(cell)

    def test_game_not_over_initially(self):
        self.assertFalse(self.game.game_over)


class TestValidPosition(unittest.TestCase):
    def setUp(self):
        self.game = tetris.Tetris()

    def test_current_piece_is_valid_at_start(self):
        self.assertTrue(self.game.valid_position(self.game.current))

    def test_invalid_position_below_board(self):
        piece = tetris.Piece([[1]], 0)
        piece.x = 0
        piece.y = tetris.ROWS  # one row below the bottom
        self.assertFalse(self.game.valid_position(piece))

    def test_invalid_position_left_of_board(self):
        piece = tetris.Piece([[1]], 0)
        piece.x = -1
        piece.y = 0
        self.assertFalse(self.game.valid_position(piece))

    def test_invalid_position_right_of_board(self):
        piece = tetris.Piece([[1]], 0)
        piece.x = tetris.COLUMNS
        piece.y = 0
        self.assertFalse(self.game.valid_position(piece))


class TestClearLines(unittest.TestCase):
    def setUp(self):
        self.game = tetris.Tetris()

    def _fill_row(self, row_index, color_index=0):
        for c in range(tetris.COLUMNS):
            self.game.grid[row_index][c] = color_index

    def test_no_clear_when_no_full_rows(self):
        self.game.clear_lines()
        self.assertEqual(self.game.lines, 0)
        self.assertEqual(self.game.score, 0)

    def test_single_line_clear(self):
        self._fill_row(tetris.ROWS - 1)
        self.game.clear_lines()
        self.assertEqual(self.game.lines, 1)
        self.assertEqual(self.game.score, 100)  # 1 * 100 * level(1)

    def test_double_line_clear(self):
        self._fill_row(tetris.ROWS - 1)
        self._fill_row(tetris.ROWS - 2)
        self.game.clear_lines()
        self.assertEqual(self.game.lines, 2)
        self.assertEqual(self.game.score, 200)  # 2 * 100 * level(1)

    def test_level_increases_after_10_lines(self):
        for i in range(10):
            self._fill_row(tetris.ROWS - 1 - i)
        self.game.clear_lines()
        self.assertEqual(self.game.lines, 10)
        self.assertEqual(self.game.level, 2)

    def test_cleared_row_replaced_by_empty_top_row(self):
        self._fill_row(tetris.ROWS - 1)
        self.game.clear_lines()
        # top row must be empty after shift
        self.assertTrue(all(cell is None for cell in self.game.grid[0]))


class TestThemeToggle(unittest.TestCase):
    def test_toggle_from_dark_to_light(self):
        game = tetris.Tetris()
        self.assertEqual(game.theme, 'dark')
        game.toggle_theme()
        self.assertEqual(game.theme, 'light')

    def test_toggle_from_light_to_dark(self):
        game = tetris.Tetris()
        game.toggle_theme()
        game.toggle_theme()
        self.assertEqual(game.theme, 'dark')


class TestRemovedUIElements(unittest.TestCase):
    """Ensure that Lines, Level, and Mode strings are not rendered on screen."""

    def _get_main_source(self):
        return inspect.getsource(tetris.main)

    def test_lines_label_not_rendered(self):
        src = self._get_main_source()
        self.assertNotIn("Lines:", src,
                         "'Lines:' label should not be rendered on screen")

    def test_level_label_not_rendered(self):
        src = self._get_main_source()
        self.assertNotIn("Level:", src,
                         "'Level:' label should not be rendered on screen")

    def test_mode_label_not_rendered(self):
        src = self._get_main_source()
        self.assertNotIn("Mode:", src,
                         "'Mode:' label (inline) should not be rendered on screen")

    def test_score_label_still_rendered(self):
        src = self._get_main_source()
        self.assertIn("Score:", src,
                      "'Score:' label should still be rendered on screen")


if __name__ == '__main__':
    unittest.main()
