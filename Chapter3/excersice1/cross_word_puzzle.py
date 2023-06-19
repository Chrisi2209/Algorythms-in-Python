import sys
sys.path.append('C:\\Programmieren\\VS_Code\\pythonAlgorithmusÜbungen\\Chapter3\\')

from csp import CSP, Constraint
from typing import List, Dict, NamedTuple, TypeVar
from random import choice
from string import ascii_uppercase
from pprint import pprint

Grid = List[List[str]]

class GridLocation(NamedTuple):
    row: int
    column: int


class WordSearchConstraint(Constraint):
    def __init__(self, words: List[str]):
        super().__init__(words)
        self.words = words

    def satisfied(self, assignment: Dict[str, List[GridLocation]]):
        # Wenn es doppelte Einträge gibt
        pprint(assignment)
        for var, loc in assignment.items():
            for index, gl in enumerate(loc):

                for var2, loc2 in assignment.items():
                    for index2, gl2 in enumerate(loc2):
                        if gl == gl2 and var[index] != var2[index2]:
                            return False
                        
        return True


        # all_locations: List[GridLocation] = [gl for gl_list in assignment.values() for gl in gl_list]
        # return len(all_locations) == len(set(all_locations))
    

def generate_grid(rows: int, columns: int) -> Grid:
    return [[choice(ascii_uppercase) for c in range(columns)] for r in range(rows)]

def display_grid(grid: Grid):
    for row in range(len(grid)):
        print("".join(grid[row]))


def generate_domain(words: List[str], grid: Grid):
    possibilities: dict[str, List[List[GridLocation]]] = {}
    width: int = len(grid[0])
    height: int = len(grid)
    for word in words:
        length: int = len(word)
        possibilities[word] = []
        for row in range(height):
            for col in range(width):
                columns: range = range(col, col + length)
                rows: range = range(row, row + length)
                if col + length <= width:
                    possibilities[word].append([GridLocation(row, c) for c in columns])

                    if row + length <= height:
                        possibilities[word].append([GridLocation(r, col + (r - row)) for r in rows])
                
                if row + length <= height:
                    possibilities[word].append([GridLocation(r, col) for r in rows])

                    if col - length >= 0:
                        possibilities[word].append([GridLocation(r, col - (r - row)) for r in rows])

        # possibilities[word] = []

        # word_length = len(word)
        # for column in range(width):
        #     if column + word_length <= width:
        #         # gerade nach rechts für alle rows
        #         for row in range(height):
        #             possibilities[word].append([GridLocation(row, column + letter_pos) for letter_pos in range(word_length)])

        #             if (row + 1) - word_length >= 0:
        #                 possibilities[word].append([GridLocation(row - letter_pos, column + letter_pos) for letter_pos in range(word_length)])

        # for row in range(height):
        #     if row + word_length <= height:
        #         # gerade nach unten
        #         for column in range(width):
        #             possibilities[word].append([GridLocation(row + letter_pos, column) for letter_pos in range(word_length)])
        #         for column in range(width):
        #             if column + word_length <= width:
        #                 # schräg nach rechts unten
        #                 possibilities[word].append([GridLocation(row + letter_pos, column + letter_pos) for letter_pos in range(word_length)])
    
    return possibilities



if __name__ == "__main__":
    words: List[str] = ["nana", "ich", "nicht", "gut", "falsch"]
    grid: Grid = generate_grid(8, 4)
    possibilities: Dict[str, List[GridLocation]] = generate_domain(words, grid)

    csp = CSP(words, possibilities)
    constraint: WordSearchConstraint = WordSearchConstraint(words)
    csp.add_constraint(constraint)   
    assignment: Dict[str, List[GridLocation]] = csp.backtracking_search()

    if assignment is not None:
        for v, loc in assignment.items():
            for index, gl in enumerate(loc):
                grid[gl.row][gl.column] = v[index]
        display_grid(grid)
    else:
        print("no solution found!")
