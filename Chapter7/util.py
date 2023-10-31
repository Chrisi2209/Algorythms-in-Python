from math import exp
from typing import List

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + exp(-x))

def derivative_sigmoid(x: float) -> float:
    sig = sigmoid(x)
    return sig * (1 - sig)

def binary_step(x: float) -> float:
    return 0 if x < 0 else 1

def binary_step_derivative(x: float) -> float:
    if x != 0:
        return 0
    else:
        raise Exception()
    
def linear(x: float) -> float:
    return 0.25 * x

def linear_derivative(x: float) -> float:
    return 0.25

def normalize_by_feature_scaling(input: List[List[float]]):
    for col in range(len(input[0])):
        column = [] 
        for row in range(len(input)):
            column.append(input[row][col])

        min_val: float = column[0]
        max_val: float = column[0]

        for entry in column:
            if entry < min_val:
                min_val = entry
            if entry > max_val:
                max_val = entry
        
        for i in range(len(column)):
            input[i][col] = (input[i][col] - min_val) / (max_val - min_val)
