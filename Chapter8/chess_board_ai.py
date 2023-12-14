from play import game_loop
import chess

from chess_board import ChessBoard

if __name__ == "__main__":
    board: chess.Board = ChessBoard()
    game_loop(board, 3, chess.Move.uci, False)