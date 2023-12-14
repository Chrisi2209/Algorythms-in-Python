from typing import List, Callable
from time import time

from board import Move, Board
from minimax import find_best_move, find_best_move_random, find_best_move_connect4_optimized


def get_human_move(board: Board, board_to_human_move: Callable[[int], Move], int_human=True) -> Move:
    human_move: Move = Move(-1)

    human_move_list: List[int] = [board_to_human_move(move)
                                  for move in board.legal_moves]

    print("possible_moves:", human_move_list)

    while human_move not in human_move_list:
        try:
            if int_human:
                human_move = int(input("your next move: "))
            else:
                human_move = input("your next move: ")
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except:
            pass

    # convert to a MOVE object
    return list(board.legal_moves)[human_move_list.index(human_move)]


def game_loop(board: Board, max_depth: int = 5, board_to_human_move: Callable[[int], int] = lambda x: x, int_human=True):
    print(board)

    while True:
        human_move: Move = get_human_move(
            board, board_to_human_move, int_human)
        board = board.move(human_move)
        print(board)
        if board.is_win:
            print("Human wins!")
            break
        if board.is_draw:
            print("Draw!")
            break

        print()

        # before = time()
        # 60s for alphabeta, 1005s for minimax (7), connect4
        # computer_move: Move = find_best_move(board, max_depth)
        computer_move: Move = find_best_move_random(board, max_depth)
        # delta = time() - before
        # human_move: Move = get_human_move(board)
        board = board.move(computer_move)
        # print("compu
        #
        # ter time:", delta)

        print(board)
        if board.is_win:
            print("Computer wins!")
            break
        if board.is_draw:
            print("Draw!")
            break

        print()


def game_loop_ai_vs_ai(board: Board, max_depth_ai1: int = 5, max_depth_ai2: int = 5):
    print(board)

    while True:
        before = time()
        computer_move: Move = find_best_move_random(board, max_depth_ai1)
        delta = time() - before
        print(f"ai1 took {round(delta, 3)}s to make its move")
        board = board.move(computer_move)
        print(board)
        if board.is_win:
            print("ai1 wins")
            break
        if board.is_draw:
            print("Draw!")
            break

        print()

        before = time()
        # 60s for alphabeta, 1005s for minimax (7), connect4
        # computer_move: Move = find_best_move(board, max_depth)
        computer_move: Move = find_best_move_random(board, max_depth_ai2)
        delta = time() - before
        print(f"ai2 took {round(delta, 3)}s to make its move")
        board = board.move(computer_move)
        # ter time:", delta)

        print(board)
        if board.is_win:
            print("ai2 wins!")
            break
        if board.is_draw:
            print("Draw!")
            break

        print()


def game_loop_connect4_optimized(board: Board, max_depth: int, board_to_human_move: Callable[[int], int] = lambda x: x):
    print(board)
    while True:
        human_move: Move = get_human_move(board, board_to_human_move)
        board = board.move(human_move)
        print(board)
        if board.is_win:
            print("human wins")
            break
        if board.is_draw:
            print("Draw!")
            break

        print()

        before = time()
        # 60s for alphabeta, 1005s for minimax (7), connect4
        # computer_move: Move = find_best_move(board, max_depth)
        computer_move: Move = find_best_move_connect4_optimized(
            board, max_depth)
        delta = time() - before
        print(f"ai took {round(delta, 3)}s to make its move")
        board = board.move(computer_move)
        # ter time:", delta)

        print(board)
        if board.is_win:
            print("ai wins!")
            break
        if board.is_draw:
            print("Draw!")
            break

        print()
