from __future__ import annotations
from typing import Generic, TypeVar, Type, Tuple, List, Callable
from chromosome import Chromosome
from enum import Enum
from random import random, randrange, choices, choice
from heapq import nlargest
from statistics import mean

C = TypeVar("C", bound=Chromosome)


class GeneticAlgorithm:
    SelectionType: Enum = Enum("SelectionType", ["Roulette", "Tournament"])

    def __init__(self, initial_population: List[C], threshhold: float, max_generations: int = 100,
                 mutation_chance: float = 0.01, crossover_chance: float = 0.7, 
                 selection_type: SelectionType = SelectionType.Tournament):
        
        self._population: List[C] = initial_population
        self._threshhold: float = threshhold
        self._max_generations: int = max_generations
        self._mutation_chance: float = mutation_chance
        self._crossover_chance: float = crossover_chance
        self._selection_type: GeneticAlgorithm.SelectionType = selection_type

        self._fitness_key: Callable = type(self._population[0]).fitness

    def roulette_winners(self, fitnesses: List[float]) -> Tuple[C, C]:
        return tuple(choices(self._population, fitnesses, k=2))
    
    def tournament_winners(self, num_participants: int) -> Tuple[C, C]:
        participants: Tuple[C] = choices(self._population, k=num_participants)
        return tuple(nlargest(2, participants, self._fitness_key))
        
    def reproduce_and_replace(self):
        new_population: List[C] = []
        
        while len(self._population) > len(new_population):
            # determine parents
            if self._selection_type == GeneticAlgorithm.SelectionType.Roulette:
                parents: Tuple[C, C] = self.roulette_winners([individual.fitness() for individual in self._population])
            else:
                parents: Tuple[C, C] = self.tournament_winners(len(self._population) // 2)

            # if crossover
            if random() < self._crossover_chance:
                new_population.extend(parents[0].crossover(parents[1]))
            # else add the parents
            else:
                new_population.extend(parents)

            
        
        if len(self._population) < len(new_population):  # if number of chromosomes is odd, this will trigger
            new_population.pop()
        
        self._population = new_population

    def mutate(self):
        for individual in self._population:
            if random() < self._mutation_chance:
                individual.mutate()

    def run(self):
        best: C = max(self._population, key=self._fitness_key)
        
        for generation in range(self._max_generations):         
            print(f"Generation={generation} best={best.fitness()} avrg={mean(map(self._fitness_key, self._population))}")
            
            if best.fitness() >= self._threshhold:
                return best
            
            self.reproduce_and_replace()
            self.mutate()

            current_best = max(self._population, key=self._fitness_key)
            if best.fitness() < current_best.fitness():
                best = current_best

        return best

