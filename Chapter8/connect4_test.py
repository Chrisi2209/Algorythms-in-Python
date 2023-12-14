import unittest

from connect4 import Connect4Board, Connect4Piece
from connect4 import c_r_index as c_r_index2
from minimax import find_best_move, find_best_move_connect4_optimized
from board import Move


def c_r_index(x, y): return c_r_index2(x, y, Connect4Board.width)


class Connect4MinimaxTest(unittest.TestCase):
    def test_easy_win(self):
        board: Connect4Board = Connect4Board(
            Connect4Piece.R, [
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.R, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.R, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.B,
                Connect4Piece.E, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.B,
            ])

        best_move: Move = find_best_move(board, 3)

        self.assertEqual(best_move, Move(4))

    def test_easy_defense(self):
        board: Connect4Board = Connect4Board(
            Connect4Piece.B, [
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.B, Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.R, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.R, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.B,
                Connect4Piece.E, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.B,
            ])

        best_move: Move = find_best_move(board, 5)

        self.assertEqual(best_move, Move(4))

    def test_hard_attack(self):
        board: Connect4Board = Connect4Board(
            Connect4Piece.R, [
                Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E,
                Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.R, Connect4Piece.E, Connect4Piece.R, Connect4Piece.B,
                Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.B, Connect4Piece.R,
                Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.R,
                Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R,
                Connect4Piece.B, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.B,
            ])

        best_move: Move = find_best_move(board, 5)

        self.assertEqual(best_move, Move(6))


class TestConnect4(unittest.TestCase):
    def test_is_win_quick2(self):
        # diagonal up right
        board: Connect4Board = Connect4Board(
            Connect4Piece.B, [
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
            ])

        self.assertEqual(board.is_win_quick(c_r_index(2, 5)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(3, 4)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(4, 3)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(5, 2)), board.is_win)

    def test_is_win_quick3(self):
        # horizontal
        board: Connect4Board = Connect4Board(
            Connect4Piece.B, [
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.R, Connect4Piece.R, Connect4Piece.R, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
            ])

        self.assertEqual(board.is_win_quick(c_r_index(0, 1)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(1, 1)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(2, 1)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(3, 1)), board.is_win)

    def test_is_win_quick4(self):
        # diagonal down right
        board: Connect4Board = Connect4Board(
            Connect4Piece.B, [
                Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.R, Connect4Piece.B, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
            ])

        self.assertEqual(board.is_win_quick(c_r_index(1, 0)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(2, 1)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(3, 2)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(4, 3)), board.is_win)

    def test_is_win_quick5(self):
        # diagonal up right false
        board: Connect4Board = Connect4Board(
            Connect4Piece.B, [
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.B, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.R, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
            ])

        self.assertEqual(board.is_win_quick(c_r_index(0, 5)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(1, 4)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(2, 3)), board.is_win)
        self.assertEqual(board.is_win_quick(c_r_index(3, 2)), board.is_win)

    def test_get_segments(self):
        # just a random board, makes no difference
        board: Connect4Board = Connect4Board(
            Connect4Piece.B, [
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.B, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.R, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
            ])

        segments_horizontal, segments_vertical, \
            segments_down_right, segments_up_right = \
            board.get_segments_for_move(0)

        self.assertEqual(segments_horizontal, [[0, 1, 2, 3]])
        self.assertEqual(segments_vertical, [
                         [c_r_index(0, 0), c_r_index(0, 1), c_r_index(0, 2), c_r_index(0, 3)]])
        self.assertEqual(segments_down_right, [
                         [c_r_index(0, 0), c_r_index(1, 1), c_r_index(2, 2), c_r_index(3, 3)]])
        self.assertEqual(segments_up_right, [])

        segments_horizontal, segments_vertical, \
            segments_down_right, segments_up_right = \
            board.get_segments_for_move(c_r_index(3, 3))

        self.assertEqual(segments_horizontal, [
            [c_r_index(0, 3), c_r_index(1, 3),
             c_r_index(2, 3), c_r_index(3, 3)],
            [c_r_index(1, 3), c_r_index(2, 3),
             c_r_index(3, 3), c_r_index(4, 3)],
            [c_r_index(2, 3), c_r_index(3, 3),
             c_r_index(4, 3), c_r_index(5, 3)],
            [c_r_index(3, 3), c_r_index(4, 3),
             c_r_index(5, 3), c_r_index(6, 3)],
        ])
        self.assertEqual(segments_vertical, [
            [c_r_index(3, 0), c_r_index(3, 1),
             c_r_index(3, 2), c_r_index(3, 3)],
            [c_r_index(3, 1), c_r_index(3, 2),
             c_r_index(3, 3), c_r_index(3, 4)],
            [c_r_index(3, 2), c_r_index(3, 3),
             c_r_index(3, 4), c_r_index(3, 5)],
        ])
        self.assertEqual(segments_down_right, [
            [c_r_index(0, 0), c_r_index(1, 1),
             c_r_index(2, 2), c_r_index(3, 3)],
            [c_r_index(1, 1), c_r_index(2, 2),
             c_r_index(3, 3), c_r_index(4, 4)],
            [c_r_index(2, 2), c_r_index(3, 3),
             c_r_index(4, 4), c_r_index(5, 5)],
        ])
        self.assertEqual(segments_up_right, [
            [c_r_index(1, 5), c_r_index(2, 4),
             c_r_index(3, 3), c_r_index(4, 2)],
            [c_r_index(2, 4), c_r_index(3, 3),
             c_r_index(4, 2), c_r_index(5, 1)],
            [c_r_index(3, 3), c_r_index(4, 2),
             c_r_index(5, 1), c_r_index(6, 0)],
        ])

    def test_easy_win(self):
        board: Connect4Board = Connect4Board(
            Connect4Piece.R, [
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.R, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.R, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.B,
                Connect4Piece.E, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.B,
            ])

        best_move: Move = find_best_move_connect4_optimized(board)

        self.assertEqual(best_move, Move(4))

    def test_easy_defense(self):
        board: Connect4Board = Connect4Board(
            Connect4Piece.B, [
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.E, Connect4Piece.E, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.B, Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.R, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.E, Connect4Piece.E,
                Connect4Piece.E, Connect4Piece.R, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.B,
                Connect4Piece.E, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.B,
            ])

        best_move: Move = find_best_move_connect4_optimized(board, 5)

        self.assertEqual(best_move, Move(4))

    def test_hard_attack(self):
        board: Connect4Board = Connect4Board(
            Connect4Piece.R, [
                Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.E, Connect4Piece.R, Connect4Piece.E,
                Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.R, Connect4Piece.E, Connect4Piece.R, Connect4Piece.B,
                Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.B, Connect4Piece.R,
                Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.R,
                Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R,
                Connect4Piece.B, Connect4Piece.B, Connect4Piece.R, Connect4Piece.R, Connect4Piece.B, Connect4Piece.B, Connect4Piece.B,
            ])

        best_move: Move = find_best_move_connect4_optimized(board, 5)

        self.assertEqual(best_move, Move(6))


if __name__ == "__main__":
    unittest.main()
