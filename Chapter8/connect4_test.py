import unittest

from connect4 import Connect4Board, Connect4Piece
from minimax import find_best_move
from board import Move


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


if __name__ == "__main__":
    unittest.main()
