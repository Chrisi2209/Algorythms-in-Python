from __future__ import annotations
from typing import Callable, List, Optional, Tuple
from random import shuffle
import numpy as np
import csv
from util import normalize_by_feature_scaling

def parse_csv(path: str, first_is_label: bool) -> Tuple(List[np.NDArray[float]], List[str]):
    with open(path, "r") as f:
        lines: List[List[str]] = list(csv.reader(f))
        shuffle(lines)
        if first_is_label:
            parameters: List[List[float]] = [np.array([float(parameter) for parameter in line[1:]]) for line in lines]
            label: List[str] = [line[0] for line in lines]
        else:
            parameters: List[List[float]] = [np.array([float(parameter) for parameter in line[:-1]]) for line in lines]
            label: List[str] = [line[-1] for line in lines]
    
    normalize_by_feature_scaling(parameters)
    
    return parameters, label
    