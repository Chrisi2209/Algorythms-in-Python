import sys
sys.path.insert(0, "C:\\Programmieren\\VS_Code\\pythonAlgorithmusÜbungen\\Chapter5")
from genetic_algorithm import GeneticAlgorithm, C
from typing import List, Tuple
from random import choices, random

class GeneticAlgorithmBetter(GeneticAlgorithm):
    def __init__(self, initial_population: List[C], threshhold: float, max_generations: int = 100,
                 mutation_chance: float = 0.03, crossover_chance: float = 0.7, 
                 selection_type: GeneticAlgorithm.SelectionType = GeneticAlgorithm.SelectionType.Tournament):
        super().__init__(initial_population, threshhold, max_generations, mutation_chance, crossover_chance, selection_type)


    def tournament_winners(self, num_participants: int) -> Tuple[C, C]:
        """
        can determine first (50%) or second (30%) or third (20%) place as the winner too
        """
        participants: List[C] = choices(self._population, k=num_participants)
        participants.sort(key=self._fitness_key, reverse=True)  # sort descending

        selector: float = random()
        if selector < 0.5:
            return tuple(participants[:2])
        elif selector < 0.8:
            return tuple(participants[1:3])
        else:
            return tuple(participants[2:4])
        

