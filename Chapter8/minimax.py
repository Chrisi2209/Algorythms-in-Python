from typing import List
from random import choice

from board import Board, Piece, Move


def minimax(board: Board, maximizing: bool,
            original_player: Piece, max_depth: int) -> float:
    #  if end of branch is reached, evaluation is done
    if max_depth == 0 or board.is_win or board.is_draw:
        return board.evaluate(original_player)

    if maximizing:
        # maximizing
        maximum = float("-inf")
        for move in board.legal_moves:
            # get evaluation of this move, next move will be minimizing
            eval = minimax(board.move(move), False,
                           original_player, max_depth - 1)

            maximum = max(maximum, eval)

        return maximum

    else:
        # minimizing
        minimum = float("inf")
        for move in board.legal_moves:
            # get evaluation for this move, next move will be maximizing
            eval = minimax(board.move(move), True,
                           original_player, max_depth - 1)

            minimum = min(minimum, eval)

        return minimum


def alphabeta(board: Board, maximizing: bool,
              original_player: Piece, max_depth: int, alpha: float = float("-inf"), beta: float = float("inf")) -> float:
    #  if end of branch is reached, evaluation is done
    if max_depth == 0 or board.is_win or board.is_draw:
        return board.evaluate(original_player)

    if maximizing:
        # maximizing
        for move in board.legal_moves:
            # get evaluation of this move, next move will be minimizing
            eval = alphabeta(board.move(move), False,
                             original_player, max_depth - 1, alpha, beta)

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return alpha

    else:
        # minimizing
        for move in board.legal_moves:
            # get evaluation for this move, next move will be maximizing
            eval = alphabeta(board.move(move), True,
                             original_player, max_depth - 1, alpha, beta)

            beta = min(beta, eval)
            if beta <= alpha:
                break

        return beta


def find_best_move_minimax(board: Board, max_depth: int = 8) -> Move:
    best_move: Move = Move(-1)
    best_eval: float = float("-inf")

    for move in board.legal_moves:
        # this player is maximizing so the next move will be minimizing
        eval = minimax(board.move(move), False, board.turn, max_depth)

        # print(f"move: {move}, eval: {eval}")

        if eval > best_eval:
            best_move = move
            best_eval = eval

    return best_move


def find_best_move(board: Board, max_depth: int = 8):
    best_move: Move = Move(-1)
    best_eval: float = float("-inf")

    for move in board.legal_moves:
        # this player is maximizing so the next move will be minimizing
        eval = alphabeta(board.move(move), False, board.turn, max_depth)

        # print(f"move: {move}, eval: {eval}")

        if eval > best_eval:
            best_move = move
            best_eval = eval

    return best_move


def find_best_move_random(board: Board, max_depth: int):
    best_moves: List[Move] = [Move(-1)]
    best_eval: float = float("-inf")

    for move in board.legal_moves:
        # this player is maximizing so the next move will be minimizing
        eval: float = alphabeta(board.move(move), False, board.turn, max_depth)

        # print(f"move: {move}, eval: {eval}")

        if eval > best_eval:
            best_moves = [move]
            best_eval = eval

        elif eval == best_eval:
            best_moves.append(move)

    return choice(best_moves)
