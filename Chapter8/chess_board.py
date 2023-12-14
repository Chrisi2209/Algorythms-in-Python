from __future__ import annotations
from typing import Optional, List, Tuple, NewType
import chess
from enum import Enum

from board import Piece, Board

ChessMove = NewType("ChessMove", str)

point_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9
}

class ChessPiece(Piece, Enum):
    W = 'W'
    B = 'B'
    E = ' '

    @property
    def opposite(self) -> ChessPiece:
        if self == ChessPiece.W:
            return ChessPiece.B
        elif self == ChessPiece.B:
            return ChessPiece.W
        else:
            return ChessPiece.E

    def __repr__(self) -> str:
        return self.value

    __str__ = __repr__


def index_c_r(index: int):
    return index % 8, index // 8

def bool_to_mul(a: bool):
    return int(a) * 2 - 1


class ChessBoard(chess.Board):
    def __init__(self, fen: Optional[str] = None, *, chess960: bool = False):
        super().__init__()
    
    def move(self, move: ChessMove) -> ChessBoard:
        if isinstance(move, str):
            move = chess.Move.from_uci(move)

        new_board = self.copy()
        new_board.push(move)
        return new_board
    
    @property
    def is_win(self) -> bool:
        return self.is_checkmate()
    
    @property
    def is_draw(self) -> bool:
        return self.is_stalemate() or self.is_insufficient_material() or \
               self.is_seventyfive_moves() or self.is_fivefold_repetition()
    
    def evaluate(self, player: bool) -> float:
        if self.is_win:
            return 1e12
        if self.is_draw:
            return 0
        
        TEMPO: float = 0.1
        # evaluation is done + for whie, - for black, in the end it is
        # relativated for player
        evaluation = 0.0
        # material
        evaluation += self.calculate_point_difference()
        # tempo
        evaluation += int(self.turn) * TEMPO if not self.is_check() else int(not self.turn) * TEMPO
        # pawn structure
        evaluation += self.pawn_eval()
        # how many threats (removed)
        # evaluation += self.eval_attacked_pieces_weighted()
        return evaluation * bool_to_mul(player)


    def pawn_eval(self) -> float:
        EVAL_FREE: float = 0.5
        EVAL_ISO: float = -0.2
        EVAL_DOUBLED: float = -0.2
        ADVANCING: float = 0.01


        white_pawn_positions = [index_c_r(square) for square in chess.SQUARES if self.piece_at(square) and 
                                self.piece_at(square).piece_type == chess.PAWN and 
                                self.piece_at(square).color == chess.WHITE]
        black_pawn_positions = [index_c_r(square) for square in chess.SQUARES if self.piece_at(square) and 
                                self.piece_at(square).piece_type == chess.PAWN and
                                self.piece_at(square).color == chess.BLACK]
        
        pawn_eval_white: float = 0
        pawn_eval_black: float = 0
        # free pawn or iso pawn
        for white_pawn, black_pawn in zip(white_pawn_positions, black_pawn_positions): 
            white_has_neighbour: bool = False
            black_has_neighbour: bool = False

            white_is_freepawn: bool = True
            black_is_freepawn: bool = True

            # more eval for more advanced pawns
            pawn_eval_white += white_pawn[1] * ADVANCING
            pawn_eval_black += black_pawn[1] * ADVANCING

            for white_pawn2, black_pawn2 in zip(white_pawn_positions, black_pawn_positions):
                if white_pawn != white_pawn2:
                    # check for isolation
                    if abs(white_pawn[0] - white_pawn2[0]) == 1:
                        white_has_neighbour = True

                    # check for double pawn
                    if white_pawn[0] - white_pawn2[0] == 0:
                        pawn_eval_black += EVAL_DOUBLED
                        
                
                if black_pawn != black_pawn2 :
                    # check for isolation
                    if abs(black_pawn[0] - black_pawn2[0]) == 1:
                        black_has_neighbour = True
                    
                    # check for double pawn
                    if black_pawn[0] - black_pawn2[0] == 0:
                        pawn_eval_black += EVAL_DOUBLED
                
                # check for free pawn
                if -2 < white_pawn[0] - black_pawn2[0] < 2:
                    white_is_freepawn = False
                
                if -2 < black_pawn[0] - white_pawn2[0] < 2:
                    black_is_freepawn = False

            if white_is_freepawn:
                pawn_eval_white += EVAL_FREE
            
            if black_is_freepawn:
                pawn_eval_black += EVAL_FREE

            if not white_has_neighbour:
                pawn_eval_white += EVAL_ISO
            
            if not black_has_neighbour:
                pawn_eval_black += EVAL_ISO
        
        return (pawn_eval_white - pawn_eval_black) / (len(black_pawn_positions) + len(white_pawn_positions)) * 0.5
    
    def eval_attacked_pieces_weighted(self) -> float:
        ATTACK: float = 0.025
        attacked_pieces_eval = 0

        # Iterate over all squares
        for square in chess.SQUARES:
            piece = self.piece_at(square)

            if piece is not None:
                attackers: List = self.attackers(not piece.color, square)
                attacked_pieces_eval += len(attackers) * ATTACK * int(not piece.color)
                                                                           
        return attacked_pieces_eval
        
    def calculate_point_difference(self) -> int:
        white_points = 0
        black_points = 0

        for square in chess.SQUARES:
            piece = self.piece_at(square)
            if piece is not None:
                if piece.color == chess.WHITE:
                    white_points += point_values.get(piece.piece_type, 0)
                else:
                    black_points += point_values.get(piece.piece_type, 0)

        return white_points - black_points

if __name__ == "__main__":
    boarder: ChessBoard = ChessBoard()
    print(boarder.evaluate(True))