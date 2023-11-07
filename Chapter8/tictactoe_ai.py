from tictactoe import TTTBoard, TTTPiece
from board import Move
from minimax import find_best_move

def get_human_move(board: TTTBoard) -> Move:
    human_move: Move = Move(-1)
    while human_move not in board.legal_moves:
        human_move = Move(int(input("your next move: ")))
    
    return human_move

if __name__ == "__main__":
    board = TTTBoard()
    print(board)

    while len(board.legal_moves) != 0:
        #computer_move: Move = find_best_move(board)
        human_move: Move = get_human_move(board)
        board = board.move(human_move)
        print(board) 
        if board.is_win:
            print("Human wins!")
            break
        if board.is_draw:
            print("Draw!")
            break

        print()

        computer_move: Move = find_best_move(board)
        #human_move: Move = get_human_move(board)
        board = board.move(computer_move)
        print(board) 
        if board.is_win:
            print("Computer wins!")
            break
        if board.is_draw:
            print("Draw!")
            break

        print()
        

