from csp import CSP, Constraint
from typing import List, Dict, NamedTuple, TypeVar

class GridLocation(NamedTuple):
    column: int
    row: int

    def __eq__(self, other):
        return self.column == other.column and self.row == other.row

class TischConstraint(Constraint):
    def __init__(self, variables):
        super().__init__(variables)
        varbs = variables

    def satisfied(self, zuweisungen: Dict, letzter_tisch_id): # zuweisungen typ: Dict[int (id): [coor, coor] (1x2)]
        last_table: List[GridLocation] = zuweisungen[letzter_tisch_id]

        s: set[GridLocation] = set()
        getSourroundingGrid(last_table[0], s)
        getSourroundingGrid(last_table[1], s)

        for key, val in zuweisungen.items():
            if key == letzter_tisch_id:
                continue
            
            for loc in val:
                if loc in s:
                    return False
        
        return True

    # def satisfied(self, zuweisungen: Dict): # zuweisungen typ: Dict[int (id): [coor, coor] (1x2)]
    #     großesUmrand = set()
    #     großesInner = set()

    #     for id, table in zuweisungen.items():
    #         kleinesUmrand = set()
    #         kleinesInner = set()
    #         kleinesInner.add(table[0])
    #         kleinesInner.add(table[1])
    #         getSourroundingGrid(table[0], kleinesUmrand)
    #         getSourroundingGrid(table[1], kleinesUmrand)

    #         for key, val in zuweisungen.items():
    #             if key == id:
    #                 continue
            
    #             for cell in kleinesInner:
    #                 if cell in großesUmrand:
    #                     return False
                    
    #                 großesInner.add(cell)
                
    #             for cell in kleinesUmrand:
    #                 if cell in großesInner:
    #                     return False
                    
    #                 großesUmrand.add(cell)
    #     return True
        
def getSourroundingGrid(gl: GridLocation, s: set):
    for x in range(-1, 2):
        for y in range(-1, 2):
            s.add(GridLocation(gl.column + x, gl.row + y))



def generate_possibilities(vars, max_x, max_y):
    possibilities: dict[str, List[List[GridLocation]]] = {}
    width: int = max_x
    height: int = max_y
    for word in vars:
        length: int = 2
        possibilities[word] = []
        for row in range(height):
            for col in range(width):
                columns: range = range(col, col + length)
                rows: range = range(row, row + length)
                if col + length <= width:
                    # waagrecht
                    possibilities[word].append([GridLocation(c, row) for c in columns])


                if row + length <= height:
                    # senkrecht
                    possibilities[word].append([GridLocation(col, r) for r in rows])

    return possibilities

def main():
    for level in range(1, 6):
        path = rf"C:\Users\chris\Downloads\level5 (4)\level5_{level}.in"
        path_out = rf"C:\Users\chris\Downloads\level5 (4)\level5_{level}.out"
        with open(path, "r") as f:
            content = f.readlines()
        
        content = content[1:]
        out = ""
        for line in content:
            values = list(map(int, line.split(" ")))
            max_x, max_y = values[0], values[1]

            vars = list(range(values[2]))
            possibilities = generate_possibilities(vars, max_x, max_y)

            csp = CSP(vars, possibilities)
            csp.add_constraint(TischConstraint(vars))
            print(f"calculating {max_x}x{max_y} with {len(vars)} tables...")
            a: Dict[int, List[GridLocation]] = csp.backtracking_search()
            out += display_grid(a, max_x, max_y) + "\n"
            print(out)
        
        with open(path_out, "w") as f:
            content = f.write(out)
    #values = list(map(8))
    # max_x, max_y =6, 6

    # vars = list(range(8))
    # possibilities = generate_possibilities(vars, max_x, max_y)

    # csp = CSP(vars, possibilities)
    # csp.add_constraint(TischConstraint(vars))
    # a: Dict[int, List[GridLocation]] = csp.backtracking_search()
    # print(display_grid(a, max_x, max_y))



def display_grid(assignment: Dict[int, List[GridLocation]], max_x, max_y):
    s = set()
    string = ""
    for v in assignment.values():
        s.add(v[0])
        s.add(v[1])
    
    for y in range(max_y):
        for x in range(max_x):
            if GridLocation(x, y) in s:
                string += "X"
            else:
                string += "."
        string += "\n"
    return string

        

if __name__ == "__main__":
    main()