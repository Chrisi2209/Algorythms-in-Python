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

if __name__ == "__main__":
    unittest.main()