from typing import List, TypeVar, Dict, Optional

V = TypeVar("V")
Possibility = TypeVar("Possibility")

class Constraint:
    def __init__(self, variables: List[V]):
        self.variables: List[V] = variables

    # you have to derive and set this method to something
    def satisfied(self, assignment: dict[V, ]):
        pass

class CSP:
    def __init__(self, variables: List[V], possibilities: Dict[V, List[Possibility]]):
        self.variables: List[V] = variables
        self.possibilities: Dict[V, List[Possibility]] = possibilities
        self.constraints: Dict[V, List[Constraint]] = {}

        self.check_integrity()

        
    def check_integrity(self):
        # if one variable has 2 domains or the length doesn't match, theres something wrong
        if len(self.possibilities.keys()) != len(set(self.possibilities.keys())) or len(self.variables) != len(self.possibilities.values()):
            raise ValueError("not every variable has a domain")
        
        # check if every variable has a domain
        for variable in self.variables:
            try:
                self.possibilities[variable]
            except(KeyError):
                raise ValueError()

    def add_constraint(self, constraint: Constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("variable in constraint not in CSP")
            else:
                self.constraints[variable] = constraint

    def backtracking_search(self, assignment: Dict[V, Possibility] = {}) -> Optional[Dict[V, Possibility]]:
        if len(assignment.keys()) == len(self.variables):
            return assignment

        unassigned: List[V] = [variable for variable in self.variables if variable not in assignment.keys()]

        next_variable = unassigned[0]

        for possibility in self.possibilities[next_variable]:
            local_assignment: Dict[V, Possibility] = assignment.copy()
            local_assignment[next_variable] = possibility

            for constraint in self.constraints[next_variable]:
                if not constraint.satisfied(local_assignment):
                    continue  # wenn possibility nicht geht dann nächste probieren
            
            result: Optional[Dict[V, Possibility]] = self.backtracking_search(local_assignment)

            if result is None:
                continue
            
            return result

        # wenn keine Lösung für dieses Assignment gefunden wurde
        return None
