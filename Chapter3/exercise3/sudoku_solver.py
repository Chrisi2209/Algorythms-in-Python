from __future__ import annotations
import sys
sys.path.append('C:\\Programmieren\\VS_Code\\pythonAlgorithmusÜbungen\\Chapter3\\')

from csp import CSP, Constraint
from typing import List, Dict, Tuple
from pprint import pprint

Sudoku = List[List[int]]
Field = int

class DifferentValueConstraint(Constraint):
    def __init__(self, fields: List[Field]):
        super().__init__(fields)
        self.fields = fields

    def satisfied(self, assignment: dict[int, int]):
        used: List[bool] = [False for _ in range(9)]

        for field in self.fields:
            try:
                if used[assignment[field] - 1] == True:
                    return False
            except KeyError:  # if field wasnt assigned yet, skip it
                continue
            
            used[assignment[field] - 1] = True
        return True
    
    def __repr__(self):
        return "<DifferentValueConstraint Fields=" + " ".join([f"[row={row} col={col}]" for row, col in [((field // 9), field % 9) for field in self.fields]]) + ">"
    
def display_fields(assignment: dict[Field, int]):
    for row in range(9):
        print("+-+-+-+-+-+-+-+-+-+")
        print("|" + "|".join([str(assignment[row * 9 + col]) for col in range(9)]) + "|")
    print("+-+-+-+-+-+-+-+-+-+")
            

def sudoku_domain(sudoku: List[List[int]]):
    domain: Dict[Field, int] = {}
    for row in range(len(sudoku)):
        for col in range(len(sudoku[0])):
            if sudoku[row][col] == 0:
                domain[row * 9 + col] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                domain[row * 9 + col] = [sudoku[row][col]]
    
    return domain


if __name__ == "__main__":
    variables: List[Field] = [i for i in range(81)]
    constraints: List[DifferentValueConstraint] = (
        [DifferentValueConstraint([(row * 9 + col) for col in range(9)]) for row in range(9)] +  # rows
        [DifferentValueConstraint([(row * 9 + col) for row in range(9)]) for col in range(9)] +  # columns
        [DifferentValueConstraint([(row * 9 + col) for row in range(3 * square_row, 3 + 3 * square_row)  for col in range(3 * square_col, 3 + 3 * square_col)]) 
         for square_col in range(3) for square_row in range(3)]  # squares
    )

    sudoku: List[List[int]] = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
    ]

    domain = sudoku_domain(sudoku)

    csp: CSP = CSP(variables, domain)
    for constraint in constraints:
        csp.add_constraint(constraint)

    assignment: Dict[Field, int] = csp.backtracking_search()
    display_fields(assignment)

    
                
