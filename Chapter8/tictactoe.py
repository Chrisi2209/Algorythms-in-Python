from __future__ import annotations
from enum import Enum
from typing import List, Tuple

from board import Board, Piece, Move

class TTTPiece(Piece, Enum):
    X = 'X'
    O = 'O'
    E = ' '

    @property
    def opposite(self) -> TTTPiece:
        if self == TTTPiece.X:
            return TTTPiece.O
        elif self == TTTPiece.O:
            return TTTPiece.X
        else:
            return TTTPiece.E
        
    def __repr__(self) -> str:
        return self.value
    
    __str__ = __repr__



def col_row_to_index(col: int, row: int) -> int:
    return col * 3 + row

def get_TTT_segments() -> List[List[Tuple]]:
    segments = []
    for col in range(3):
        segments.append([col_row_to_index(col, 0), col_row_to_index(col, 1), col_row_to_index(col, 2)])

    for row in range(3):
        segments.append([col_row_to_index(0, row), col_row_to_index(1, row), col_row_to_index(2, row)])
    
    segments.append([col_row_to_index(0, 0), col_row_to_index(1, 1), col_row_to_index(2, 2)])
    segments.append([col_row_to_index(0, 2), col_row_to_index(1, 1), col_row_to_index(2, 0)])
    
    return segments



class TTTBoard(Board):
    segments = get_TTT_segments()

    def __init__(self, turn: TTTPiece = TTTPiece.X, position: List[TTTPiece] = [TTTPiece.E] * 9) -> None:
        self._turn = turn
        self.position: List[TTTPiece] = position

    @property
    def turn(self) -> TTTPiece:
        return self._turn
    
    def move(self, location: Move) -> TTTBoard:
        temp_position: List[TTTPiece] = self.position.copy()
        temp_position[location] = self.turn
        return TTTBoard(self.turn.opposite, temp_position)
    
    @property
    def legal_moves(self) -> List[Move]:
        return [Move(l) for l in range(len(self.position)) if self.position[l] == TTTPiece.E]

    
    def segment_monocolour(self, segment: List[Tuple]):
        for first, second in zip(segment, segment[1:]):
            if not (self.position[first] == self.position[second] != TTTPiece.E):
                return False
        
        return True

    @property
    def is_win(self) -> bool:
        for segment in TTTBoard.segments:
            if self.segment_monocolour(segment):
                return True
        
        return False
    
    def evaluate(self, player: TTTPiece) -> float:
        # the player whose turn it is has lost, so if player is on the turn, evaluation is -1, if no win, evaluation is 0
        return int(self.is_win) * (1 - (2 * int(self.turn == player)))
    
    def __repr__(self):
        return f"""-------
|{self.position[0]}|{self.position[1]}|{self.position[2]}|
-------
|{self.position[3]}|{self.position[4]}|{self.position[5]}|
-------
|{self.position[6]}|{self.position[7]}|{self.position[8]}|
-------"""
        
