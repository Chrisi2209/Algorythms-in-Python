from __future__ import annotations
from typing import Callable, List, Optional, Tuple
from random import random
import numpy as np
import csv

def parse_csv(path: str, first_is_label: bool) -> Tuple(List[List[float], List[str]]):
    with open(path, "r") as f:
        lines: List[List[str]] = list(csv.reader(f))
        if first_is_label:
            parameters: List[List[float]] = [[float(parameter) for parameter in line[1:]] for line in lines]
            label: List[str] = [line[1] for line in lines]
        else:
            parameters: List[List[float]] = [[float(parameter) for parameter in line[:-1]] for line in lines]
            label: List[str] = [line[-1] for line in lines]
    
    return parameters, label
    