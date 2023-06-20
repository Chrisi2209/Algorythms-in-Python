from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Tuple

T = TypeVar("T", bound="Chromosome")

class Chromosome(ABC):
    @abstractmethod
    def fitness(self):
        pass

    @classmethod
    @abstractmethod
    def random_instance(cls: Type[T]) -> T:
        pass

    @abstractmethod
    def mutate(self):
        pass

    @abstractmethod
    def crossover(self: T, other: T) -> Tuple[T, T]:
        pass
