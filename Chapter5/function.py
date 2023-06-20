from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Tuple
from random import randint, random
from copy import deepcopy

from excersice1 import genetic_algorithm_better
from chromosome import Chromosome

T = TypeVar("T", bound="Chromosome")

class FunctionChromosome(Chromosome):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def fitness(self):
        return 6 * self.x +- self.x * self.x + 4 * self.y - self.y * self.y

    @classmethod
    def random_instance(cls: Type[T]) -> T:
        return FunctionChromosome(randint(0, 100), randint(0, 100))

    def mutate(self):
        if random() < 0.5:
            if random() < 0.5:
                self.x += 1
            else:
                self.x -= 1
        else:
            if random() < 0.5:
                self.y += 1
            else:
                self.y -= 1

    def crossover(self: Chromosome, other: Chromosome) -> Tuple[T, T]:
        child1 = deepcopy(self)
        child2 = deepcopy(other)

        child1.y, child2.y = child2.y, child1.y

        return child1, child2


def find_maxima():
    ga = genetic_algorithm_better.GeneticAlgorithmBetter(
        [FunctionChromosome.random_instance() for _ in range(100)],
        13.0,
        100,
    )

    result: Chromosome = ga.run()

    print(f"x={result.x} y={result.y}")


if __name__ == "__main__":
    find_maxima()

