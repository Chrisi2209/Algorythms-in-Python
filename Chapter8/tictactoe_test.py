import unittest

from tictactoe import TTTBoard, TTTPiece
from minimax import find_best_move
from board import Move


class TTTMinimaxTestCase(unittest.TestCase):
    def test_easy_defending(self):
        board: TTTBoard = TTTBoard(TTTPiece.X, [TTTPiece.X, TTTPiece.O, TTTPiece.E,
                                                TTTPiece.E, TTTPiece.O, TTTPiece.X,
                                                TTTPiece.E, TTTPiece.E, TTTPiece.E])

        best_move: Move = find_best_move(board)
        self.assertEqual(best_move, Move(7))

    def test_easy_attacking(self):
        board: TTTBoard = TTTBoard(TTTPiece.O, [TTTPiece.O, TTTPiece.E, TTTPiece.X,
                                                TTTPiece.E, TTTPiece.X, TTTPiece.E,
                                                TTTPiece.O, TTTPiece.E, TTTPiece.X])

        best_move: Move = find_best_move(board)
        self.assertEqual(best_move, Move(3))

    def test_hard_winning_position(self):
        board: TTTBoard = TTTBoard(TTTPiece.X, [TTTPiece.X, TTTPiece.E, TTTPiece.E,
                                                TTTPiece.E, TTTPiece.E, TTTPiece.O,
                                                TTTPiece.O, TTTPiece.X, TTTPiece.E])

        best_move: Move = find_best_move(board)
        self.assertIn(best_move, (Move(1), Move(4)))


# exercise 1
class TTTMinimaxTestCase(unittest.TestCase):
    def test_is_win_false(self):
        board: TTTBoard = TTTBoard(TTTPiece.X, [TTTPiece.X, TTTPiece.E, TTTPiece.X,
                                                TTTPiece.O, TTTPiece.X, TTTPiece.O,
                                                TTTPiece.O, TTTPiece.X, TTTPiece.O])

        self.assertEqual(board.is_win, False)

    def test_is_win_true(self):
        board: TTTBoard = TTTBoard(TTTPiece.X, [TTTPiece.O, TTTPiece.X, TTTPiece.X,
                                                TTTPiece.X, TTTPiece.X, TTTPiece.O,
                                                TTTPiece.O, TTTPiece.X, TTTPiece.O])

        self.assertEqual(board.is_win, True)

    def test_is_draw_true(self):
        board: TTTBoard = TTTBoard(TTTPiece.X, [TTTPiece.X, TTTPiece.O, TTTPiece.X,
                                                TTTPiece.X, TTTPiece.X, TTTPiece.O,
                                                TTTPiece.O, TTTPiece.X, TTTPiece.O])

        self.assertEqual(board.is_draw, True)

    def test_is_draw_false(self):
        board: TTTBoard = TTTBoard(TTTPiece.X, [TTTPiece.O, TTTPiece.X, TTTPiece.X,
                                                TTTPiece.O, TTTPiece.O, TTTPiece.X,
                                                TTTPiece.X, TTTPiece.X, TTTPiece.O])

        self.assertEqual(board.is_draw, False)

    def test_legal_moves(self):
        board: TTTBoard = TTTBoard(TTTPiece.X, [TTTPiece.X, TTTPiece.E, TTTPiece.E,
                                                TTTPiece.E, TTTPiece.E, TTTPiece.O,
                                                TTTPiece.O, TTTPiece.X, TTTPiece.E])

        self.assertEqual(board.legal_moves, [Move(
            1), Move(2), Move(3), Move(4), Move(8)])


if __name__ == "__main__":
    unittest.main()
