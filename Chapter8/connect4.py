from __future__ import annotations
from enum import Enum
from typing import List, Tuple

from board import Board, Piece, Move


class Connect4Piece(Piece, Enum):
    R = 'R'
    B = 'B'
    E = ' '

    @property
    def opposite(self) -> Connect4Piece:
        if self == Connect4Piece.R:
            return Connect4Piece.B
        elif self == Connect4Piece.B:
            return Connect4Piece.R
        else:
            return Connect4Piece.E

    def __repr__(self) -> str:
        return self.value

    __str__ = __repr__


def c_r_index(col: int, row: int, width: int) -> int:
    return col + row * width


def get_segments(width: int, height: int, length: int) -> List[List[int]]:
    segments: List[List[int]] = []
    # vertikal
    for x in range(width):
        new_segments: List[List[int]] = []
        for start_y in range(0, height - length + 1):
            new_segments.append([c_r_index(x, y, width)
                                for y in range(start_y, start_y + length)])

        segments.extend(new_segments)

    # horizontal
    for y in range(height):
        new_segments: List[List[int]] = []
        for start_x in range(0, width - length + 1):
            new_segments.append([c_r_index(x, y, width)
                                for x in range(start_x, start_x + length)])

        segments.extend(new_segments)

    # diagonal down right
    for start_x in range(width - length + 1):
        new_segments: List[List[int]] = []
        for start_y in range(height - length + 1):
            x_range: range = range(start_x, start_x + length)
            y_range: range = range(start_y, start_y + length)
            new_segments.append([c_r_index(x, y, width)
                                for x, y in zip(x_range, y_range)])

        segments.extend(new_segments)

    # diagonal up right
    for start_x in range(width - length + 1):
        new_segments: List[List[int]] = []
        for start_y in range(length - 1, height):
            x_range: range = range(start_x, start_x + length)
            y_range: range = range(start_y, start_y - length, -1)
            new_segments.append([c_r_index(x, y, width)
                                for x, y in zip(x_range, y_range)])

        segments.extend(new_segments)

    return segments


class Connect4Board(Board):
    width: int = 7
    height: int = 6
    win_length: int = 4
    segments: List[List[int]] = get_segments(width, height, win_length)

    def __init__(self, turn: Connect4Piece = Connect4Piece.R,
                 position: List[Connect4Piece] = [Connect4Piece.E] * width * height) -> None:
        self._turn = turn
        self.position: List[Connect4Piece] = position

    @property
    def turn(self) -> Connect4Piece:
        return self._turn

    def move(self, location: Move) -> Connect4Board:
        temp_position: List[Connect4Piece] = self.position.copy()
        temp_position[location] = self.turn
        return Connect4Board(self.turn.opposite, temp_position)

    @property
    def legal_moves(self) -> List[Move]:
        legal_moves: List[Move] = []

        for col in range(self.width):
            if self.position[c_r_index(col, 0, self.width)] != Connect4Piece.E:
                # column is full, next one
                continue

            # get first free row of this column
            for line in range(self.height - 1, -1, -1):
                index: int = c_r_index(col, line, self.width)
                if self.position[index] == Connect4Piece.E:
                    # first free position found
                    legal_moves.append(Move(index))
                    break

        return legal_moves

    def count_segment(self, segment: List[int]) -> Tuple[int, int]:
        red_count: int = 0
        blue_count: int = 0

        for index in segment:
            if self.position[index] == Connect4Piece.R:
                red_count += 1

            elif self.position[index] == Connect4Piece.B:
                blue_count += 1

        return red_count, blue_count

    def segment_monocolour(self, segment: List[Tuple]):
        for first, second in zip(segment, segment[1:]):
            if not (self.position[first] == self.position[second] != Connect4Piece.E):
                return False

        return True

    @property
    def is_win(self) -> bool:
        for segment in self.segments:
            if self.segment_monocolour(segment):
                return True

        return False

    def evaluate(self, player: Connect4Piece) -> float:
        eval: float = 0
        for segment in self.segments:
            red_count, blue_count = self.count_segment(segment)

            if red_count > 0 and blue_count > 0:
                # segments with both colours count nothing
                continue

            # if red_count > 0:
            #     if player == Connect4Piece.R:
            #         for_you = 1
            #     else:
            #         for_you = -1

            # else:
            #     if player == Connect4Piece.R:
            #         for_you = -1
            #     else:
            #         for_cou = 1

            multiplicator: int = (
                int(player == Connect4Piece.R) * 2 - 1) * (int(red_count > 0) * 2 - 1)

            count: int = max(red_count, blue_count)

            # könnte auch Faktor von unendlich machen, nur zählen wer am meisten
            # vom meisten hat.

            if count == 0:
                continue

            if count == 1:
                eval += 1 * multiplicator

            elif count == 2:
                eval += 100 * multiplicator

            elif count == 3:
                eval += 1_000_000 * multiplicator

            elif count == 4:
                eval += 1_000_000_000_000 * multiplicator

        return eval

    def __repr__(self):
        out: str = ""
        out += "-" + "".join("--" for _ in range(self.width)) + "\n"
        for row in range(self.height):
            out += "|"
            out += "|".join(str(self.position[c_r_index(
                col, row, self.width)]) for col in range(self.width))
            out += "|\n"
        out += "-" + "".join("--" for _ in range(self.width))

        return out
