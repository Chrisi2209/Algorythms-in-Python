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

    # optimized_functions
    def get_segments_for_move(self, move: Move) -> Tuple[List[List[int]], List[List[int]], List[List[int]], List[List[int]]]:
        last_move_col: int = move % self.width
        last_move_row: int = move // self.width

        segments_horizontal: List[List[int]] = [[c_r_index(x, last_move_row, self.width)
                                                 for x in range(last_move_col - self.win_length + i, last_move_col + i)]
                                                for i in range(1, self.win_length + 1)
                                                # <= self.width because it will only go win_length - 1 towards the edge
                                                if 0 <= last_move_col - self.win_length + i and last_move_col + i <= self.width]

        segments_vertical: List[List[int]] = [[c_r_index(last_move_col, y, self.width)
                                               for y in range(last_move_row - self.win_length + i, last_move_row + i)]
                                              for i in range(1, self.win_length + 1)
                                              if 0 <= last_move_row - self.win_length + i and last_move_row + i <= self.height]

        segments_down_right: List[List[int]] = [[c_r_index(x, y, self.width)
                                                 for x, y in zip(
                                                     range(
                                                         last_move_col - self.win_length + i, last_move_col + i),
                                                     range(
                                                         last_move_row - self.win_length + i, last_move_row + i),
        )]
            for i in range(1, self.win_length + 1)
            if 0 <= last_move_col - self.win_length + i and last_move_col + i <= self.width and
            0 <= last_move_row - self.win_length + i and last_move_row + i <= self.height]

        segments_up_right: List[List[int]] = [[c_r_index(x, y, self.width)
                                               for x, y in zip(
            range(last_move_col - self.win_length + i, last_move_col + i),
            range(last_move_row + (self.win_length - i),
                  last_move_row - self.win_length + (self.win_length - i), -1),
        )]
            for i in range(1, self.win_length + 1)
            if 0 <= last_move_col - self.win_length + i and last_move_col + i <= self.width and
            0 <= last_move_row - self.win_length + (self.win_length - i) + 1 and last_move_row + (self.win_length - i) < self.height]

        return segments_horizontal, segments_vertical, segments_down_right, segments_up_right

    def is_win_quick(self, last_move: Move):
        last_move_col: int = last_move % self.width
        last_move_row: int = last_move // self.width
        # horizontal

        horizontal_counter: int = 0
        vertical_counter: int = 0
        # top left to bottom right diagonal
        diagonal_down_counter: int = 0
        # bottom left to top right diagonal
        diagonal_up_counter: int = 0

        for x, y_top, y_bot in zip(
            range(last_move_col - self.win_length +
                  2, last_move_col + self.win_length),
            range(last_move_row - self.win_length +
                  2, last_move_row + self.win_length),
            range(last_move_row + self.win_length - 2,
                  last_move_row - self.win_length, -1)
        ):
            # 0 <<< because it has to be at least one for the comparison not to fail
            # later down the line. (1 is substracted there)
            x_in_bounds: bool = 0 < x < self.width
            y_top_in_bounds: bool = 0 < y_top < self.height
            # because it is only used in diagonal bottom left to top right, and it is handy to have it stop at height -1 for there, we let it limited to there
            y_bot_in_bounds: bool = 0 < y_bot < self.height - 1

            # horizontal
            if x_in_bounds:
                if self.position[c_r_index(x - 1, last_move_row, self.width)] == self.position[c_r_index(x, last_move_row, self.width)] != Connect4Piece.E:
                    horizontal_counter += 1
                    if horizontal_counter == self.win_length - 1:
                        return True
                else:
                    horizontal_counter = 0

            # vertical
            if y_top_in_bounds:
                if self.position[c_r_index(last_move_col, y_top - 1, self.width)] == self.position[c_r_index(last_move_col, y_top, self.width)] != Connect4Piece.E:
                    vertical_counter += 1
                    if vertical_counter == self.win_length - 1:
                        return True
                else:
                    vertical_counter = 0

            # diagonal top left to bottom right
            if y_top_in_bounds and x_in_bounds:
                if self.position[c_r_index(x - 1, y_top - 1, self.width)] == self.position[c_r_index(x, y_top, self.width)] != Connect4Piece.E:
                    diagonal_down_counter += 1
                    if diagonal_down_counter == self.win_length - 1:
                        return True
                else:
                    diagonal_down_counter = 0

            # diagonal top left to bottom right
            if y_bot_in_bounds and x_in_bounds:
                if self.position[c_r_index(x - 1, y_bot + 1, self.width)] == self.position[c_r_index(x, y_bot, self.width)] != Connect4Piece.E:
                    diagonal_up_counter += 1
                    if diagonal_up_counter == self.win_length - 1:
                        return True
                else:
                    diagonal_up_counter = 0

        # if no one wins because of this turn, return false
        return False

    def is_draw_quick(self, last_move: Move):
        return (len(self.legal_moves) == 0) and (not self.is_win_quick(last_move))

    def evaluate_quick(self, player: Connect4Piece, last_move: Move, last_eval: float) -> None:
        # if self.is_win_quick(last_move):
        #     return 1_000_000_000_000_000 * (int(player == Connect4Piece.R) * 2 - 1)

        # elif self.is_draw_quick(last_move):
        #     return 0

        # # get_segments_containing_position(last_move), evaluate these segments and add it to last eval? <- still has problems
        # for segment in self.segments:
        #     pass

        # player = the player for whom we evaluate
        # last move, the last position, a chip was placed
        # last eval, the eval before the move was played

        def count_to_score(count):
            if count <= 0:
                return 0
            if count == 1:
                return 1
            if count == 2:
                return 100
            if count == 3:
                return 700
            if count == self.win_length:
                return 10e12

            return 3 ** (count)

        eval_diff: int = 0

        segments: List[List[int]] = sum(
            self.get_segments_for_move(last_move), start=[])

        for segment in segments:
            red_count, blue_count = self.count_segment(segment)

            # assign the counts to the player thats turn it is and not.
            moved_player: Connect4Piece = self.position[last_move]
            if moved_player == Connect4Piece.B:
                turn_count: int = blue_count
                not_turn_count: int = red_count
            else:
                turn_count: int = red_count
                not_turn_count: int = blue_count

            # check if this segment was destroyed by this turn
            if turn_count == 1 and not_turn_count > 0:
                # If the moved player is player, he made +, so this is added
                eval_diff += count_to_score(not_turn_count) * \
                    ((moved_player == player) * 2 - 1)

            # if this move made this segment larger
            elif turn_count > 0 and not_turn_count == 0:
                # Add the score to the player who made the move
                eval_diff += count_to_score(turn_count) * \
                    ((moved_player == player) * 2 - 1)

            # If the Segment was destroyed earlier
            # elif turn_count > 1 and not_turn_count > 1:
            #     # do nothing
            #     pass

        return last_eval + eval_diff

    """ This was part of the old evaluate_quick
        for x, y_top, y_bot in zip(
            range(last_move_col - self.win_length +
                  2, last_move_col + self.win_length),
            range(last_move_row - self.win_length +
                  2, last_move_row + self.win_length),
            range(last_move_row + self.win_length - 2,
                  last_move_row - self.win_length, -1)
        ):
            # 0 <<< because it has to be at least one for the comparison not to fail
            # later down the line. (1 is substracted there)
            x_in_bounds: bool = 0 < x < self.width
            y_top_in_bounds: bool = 0 < y_top < self.height
            # because it is only used in diagonal bottom left to top right, and it is handy to have it stop at height -1 for there, we let it limited to there
            y_bot_in_bounds: bool = 0 < y_bot < self.height - 1

            # horizontal
            if x_in_bounds:
                if self.position[c_r_index(x - 1, last_move_row, self.width)] == self.position[c_r_index(x, last_move_row, self.width)]:
                    evaluation_delta += 10 ** (2 * horizontal_counter)
                    horizontal_counter += 1
                    if horizontal_counter == self.win_length:
                        return 1_000_000_000
                else:
                    # _, 2, 3, 4!
                    for i in range(2, min(horizontal_counter, 4) + 1):
                        evaluation_delta -= 10 ** (2 * (i - 1))

                    horizontal_counter = 1

            # vertical
            if y_top_in_bounds:
                if self.position[c_r_index(last_move_col, y_top - 1, self.width)] == self.position[c_r_index(last_move_col, y_top, self.width)] != Connect4Piece.E:
                    vertical_counter += 1
                    if vertical_counter == self.win_length - 1:
                        return True
                else:
                    vertical_counter = 0

            # diagonal top left to bottom right
            if y_top_in_bounds and x_in_bounds:
                if self.position[c_r_index(x - 1, y_top - 1, self.width)] == self.position[c_r_index(x, y_top, self.width)] != Connect4Piece.E:
                    diagonal_down_counter += 1
                    if diagonal_down_counter == self.win_length - 1:
                        return True
                else:
                    diagonal_down_counter = 0

            # diagonal top left to bottom right
            if y_bot_in_bounds and x_in_bounds:
                if self.position[c_r_index(x - 1, y_bot + 1, self.width)] == self.position[c_r_index(x, y_bot, self.width)] != Connect4Piece.E:
                    diagonal_up_counter += 1
                    if diagonal_up_counter == self.win_length - 1:
                        return True
                else:
                    diagonal_up_counter = 0

        # if no one wins because of this turn, return false

        return evaluation_delta
    """

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
