from connect4 import Connect4Board
from play import game_loop, game_loop_ai_vs_ai, game_loop_connect4_optimized


def get_index_to_col(width: int):

    def index_to_col(index: int):
        return index % width

    return index_to_col


if __name__ == "__main__":
    count = 4
    print(10 ** (count * 3) if count > 0 else 0)
    board = Connect4Board()
    # game_loop_ai_vs_ai(board, 2, 6)
    game_loop_connect4_optimized(board, 42, get_index_to_col(board.width))
