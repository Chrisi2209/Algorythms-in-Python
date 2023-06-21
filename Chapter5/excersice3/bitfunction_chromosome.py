from __future__ import annotations
from typing import Generic, TypeVar, Type, Tuple
from random import randint
from copy import deepcopy
import sys

sys.path.insert(0, "C:\\Programmieren\\VS_Code\\pythonAlgorithmusÜbungen\\Chapter5\\")
from bitstring import BitString
from genetic_algorithm import GeneticAlgorithm
from chromosome import Chromosome

class BitfunctionChromosome(Chromosome):
    def __init__(self, x, y):
        self.bitstring = BitString(x + y * 256 + 0b10000000000000000)

    @property
    def x(self) -> int:
        return int(self.bitstring[0:8])
    
    @property
    def y(self) -> int:
        return int(self.bitstring[8:16])
    
    @property
    def binstring(self) -> str:
        return self.bitstring.binstring.zfill(16)
    

    def fitness(self):
        return 6 * self.x - self.x * self.x + 4 * self.y - self.y * self.y

    @classmethod
    def random_instance(cls: BitfunctionChromosome) -> BitfunctionChromosome:
        return BitfunctionChromosome(randint(0, 100), randint(0, 100))

    def mutate(self):
        self.bitstring.invert(randint(0, 15))

    def crossover(self: BitfunctionChromosome, 
                  other: BitfunctionChromosome) -> Tuple[BitfunctionChromosome, BitfunctionChromosome]:
        bit: int = randint(0, 15)

        child1 = deepcopy(self)
        child2 = deepcopy(other)

        child1.bitstring[bit], child2.bitstring[bit] = child2.bitstring[bit], child1.bitstring[bit]

        return child1, child2


def find_maxima():
    ga = GeneticAlgorithm(
        [BitfunctionChromosome.random_instance() for _ in range(400)],
        threshhold=13.0,
        mutation_chance=0.02,
    )
    result: BitfunctionChromosome = ga.run()
    print(result.bitstring.binstring)

    print(f"x={result.x} y={result.y} result={result.fitness()}")

if __name__ == "__main__":
    # print(int("", base=2))
    # a = BitfunctionChromosome(3, 3)
    # print(a.x, a.y)
    find_maxima()
