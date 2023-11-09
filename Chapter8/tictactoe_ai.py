from typing import Dict

from tictactoe import TTTBoard
from board import Move
from play import game_loop


def board_to_human_move(human_move: Move):
    numpad_to_move: Dict[int, int] = {
        0: 7,
        1: 8,
        2: 9,
        3: 4,
        4: 5,
        5: 6,
        6: 1,
        7: 2,
        8: 3,
    }

    return numpad_to_move[human_move]


if __name__ == "__main__":
    board = TTTBoard()
    game_loop(board, 8)
