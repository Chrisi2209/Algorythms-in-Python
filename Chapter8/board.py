from __future__ import annotations
from abc import ABC, abstractmethod
from typing import NewType, List

Move = NewType('Move', int)

class Piece:
    @property
    def opposite(self) -> Piece:
        raise NotImplementedError("please implement by deriving from this class")


class Board(ABC):
    @property
    @abstractmethod
    def turn(self) -> Piece:
        raise NotImplementedError("please implement by deriving from this class")
    
    @abstractmethod
    def move(self, move: Move) -> Board:
        raise NotImplementedError("please implement by deriving from this class")
    
    @property
    @abstractmethod
    def legal_moves(self) -> List[Move]:
        raise NotImplementedError("please implement by deriving from this class")
    
    @property
    @abstractmethod
    def is_win(self) -> bool:
        raise NotImplementedError("please implement by deriving from this class")
    
    @property
    def is_draw(self) -> bool:
        return (len(self.legal_moves) == 0) and (not self.is_win)
    
    @abstractmethod
    def evaluate(self, player: Piece) -> float:
        raise NotImplementedError("please implement by deriving from this class")
    

