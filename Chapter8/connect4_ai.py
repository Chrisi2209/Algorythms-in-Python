from connect4 import Connect4Board
from play import game_loop, game_loop_ai_vs_ai


def get_index_to_col(width: int):

    def index_to_col(index: int):
        return index % width

    return index_to_col


if __name__ == "__main__":
    board = Connect4Board()
    game_loop_ai_vs_ai(board, 2, 6)
