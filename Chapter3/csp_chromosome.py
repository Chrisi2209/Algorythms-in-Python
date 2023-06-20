from __future__ import annotations
import sys
sys.path.insert(0, "C:\\Programmieren\\VS_Code\\pythonAlgorithmusÜbungen\\Chapter5")
from chromosome import Chromosome
from typing import Callable, Dict, TypeVar, List
from random import randint, choice, randrange, choices
from copy import deepcopy

V = TypeVar("V")
Possibility = TypeVar("Possibility")

class CspChromosome(Chromosome):
    def __init__(self, assignment: Dict[V, Possibility],
                 possibilities: Dict[V, List[Possibility]], 
                 fitness_func: Callable):
        self._fitness_func: Callable = fitness_func
        self._assignment: Dict[V, Possibility] = assignment
        self._possibilities: Dict[V, List[Possibility]] = possibilities
    
    @classmethod
    def random_instance(cls: CspChromosome, possibilities: Dict[V, List[Possibility]], fitness_func: Callable) -> CspChromosome: 
        assignment: Dict[V, int] = {}
        for variable, possibilitieses in possibilities.items():
            assignment[variable] = choice(possibilitieses)
        
        return CspChromosome(assignment, possibilities, fitness_func)

    def mutate(self):
        # select a variable to mutate
        mutating_var: V = choice(list(self._assignment.keys()))

        # mutate variable to random possibility
        self._assignment[mutating_var] = choice(self._possibilities[mutating_var])

    def crossover(self, other: CspChromosome):
        crossover_variable: V = choice(list(self._possibilities.keys()))

        child1 = self.copy()
        child2 = other.copy()

        child1._assignment[crossover_variable], child2._assignment[crossover_variable] = \
            other._assignment[crossover_variable], self._assignment[crossover_variable]

        return child1, child2

    def fitness(self) -> float:
        return self._fitness_func(self)
    
    def copy(self) -> CspChromosome:
        return CspChromosome(
            self._assignment.copy(),
            self._possibilities,
            self._fitness_func
        )
    
    def possibilitylengthok(self):
        for v, l in self._assignment.items():
            if len(l) != len(v):
                return False
        
        return True
