from __future__ import annotations
import sys
sys.path.append('C:\\Programmieren\\VS_Code\\pythonAlgorithmusÜbungen\\kap3\\')

from csp import CSP, Constraint
from typing import List, Dict, NamedTuple, TypeVar
from random import choice
from string import ascii_uppercase
from pprint import pprint

Grid = List[List[int]]

class GridLocation(NamedTuple):
    row: int
    column: int
    

class Chip():
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

    # def __eq__(self, other: Chip):
    #     return (self.width == other.width and self.height == other.height)


class ChipSearchConstraint(Constraint):
    def __init__(self, chips: List[Chip]):
        super().__init__(chips)
        self.chips = chips
    
    def satisfied(self, assignment: dict[Chip, List[List[GridLocation]]]):
        for chip1, gl1 in assignment.items():
            gl_list1: List[GridLocation] = [gl for gl_list in gl1 for gl in gl_list]
            for chip2, gl2 in assignment.items():
                gl_list2: List[GridLocation] = [gl for gl_list in gl2 for gl in gl_list]
                concatinated: List[GridLocation] = gl_list1 + gl_list2
                
                if chip1 != chip2 and len(concatinated) != len(set(concatinated)):
                    return False
        
        return True    
    

def generate_domain(chips: List[Chip]) -> Dict[Chip, List[List[List[GridLocation]]]]:
    possibilities: dict[Chip, List[List[List[GridLocation]]]] = {}
    width: int = len(grid[0])
    height: int = len(grid)
    for chip in chips:
        possibilities[chip] = []

        for row in range(height):
            for col in range(width):
                if row + chip.height <= height and col + chip.width <= width:
                    possibilities[chip].append([[GridLocation(r, c) for c in range(col, col + chip.width)] 
                                                for r in range(row, row + chip.height)])

    return possibilities

def generate_grid(rows: int, columns: int) -> Grid:
    return [[0 for c in range(columns)] for r in range(rows)]

def assignment_to_grid(grid: Grid, assignment: Dict[Chip, List[List[GridLocation]]]):
    for id, gl in enumerate(assignment.values()):
        for gl_row in gl:
            for gl in gl_row:
                grid[gl.row][gl.column] = id + 1

def display_grid(grid: Grid):
    for row in grid:
        print("".join([str(id) for id in row]))
        

if __name__ == "__main__":
    chips: List[Chip] = [Chip(2, 3), Chip(1, 3), Chip(3, 4), Chip(3, 3), Chip(3, 2), Chip(2, 2), Chip(3, 2), Chip(1, 2)] # 2 mit selber breite unf Höhe
    grid: Grid = generate_grid(7, 7)
    domain = generate_domain(chips)
    csp = CSP(chips, domain)
    constraint: ChipSearchConstraint = ChipSearchConstraint(chips)
    csp.add_constraint(constraint)

    assignment: Dict[Chip, GridLocation] = csp.backtracking_search()

    if assignment is not None:
        assignment_to_grid(grid, assignment)
        display_grid(grid)
    else:
        print("no solution found!")
