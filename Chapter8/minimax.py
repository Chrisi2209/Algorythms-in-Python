from board import Board, Piece, Move


def minimax(board: Board, maximizing: bool, original_player: Piece, max_depth: int) -> float:
    #  if end of branch is reached, evaluation is done
    if max_depth == 0 or board.is_win or board.is_draw:
        return board.evaluate(original_player)
    
    
    if maximizing:
        # maximizing
        maximum = float("-inf")
        for move in board.legal_moves:
            # get evaluation of this move, next move will be minimizing
            eval = minimax(board.move(move), False, original_player, max_depth - 1)
            maximum = max(maximum, eval)
        
        return maximum

    else:
        # minimizing
        minimum = float("inf")
        for move in board.legal_moves:
            # get evaluation for this move, next move will be maximizing
            eval = minimax(board.move(move), True, original_player, max_depth - 1)
            minimum = min(minimum, eval)
        
        return minimum


def find_best_move(board: Board):
    best_move: Move = Move(-1)
    best_eval: float = float("-inf")

    for move in board.legal_moves:
        # this player is maximizing so the next move will be minimizing
        eval = minimax(board.move(move), False, board.turn, 8)

        #print(f"move: {move}, eval: {eval}")

        if eval > best_eval:
            best_move = move
            best_eval = eval
    
    return best_move