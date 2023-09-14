from __future__ import annotations
from typing import Iterable
from math import sqrt


class DataPoint:
    """
    A data point is a point in an n-dimensional space defined by
    the length of the initial iterable.
    """
    def __init__(self, initial: Iterable[float]) -> None:
        self._original = tuple(initial)
        self.dimensions = tuple(initial)

    def distance(self, other: DataPoint) -> float:
        """returns the distance between self and an other data point"""
        differences = [(self.dimensions[dim] - other.dimensions[dim]) ** 2 for dim in range(self.num_dimensions)]
        return sqrt(sum(differences))
    
    @property
    def num_dimensions(self):
        return len(self.dimensions)
    
    def __eq__(self, other: DataPoint) -> bool:
        if not isinstance(other, DataPoint):
            return NotImplemented
        
        return self.dimensions == other.dimensions

    def __repr__(self) -> str:
        return f"<Datapoint dimensions=[{', '.join(map(str, map(round, self._original, [2] * len(self.dimensions))))}]>"
    
