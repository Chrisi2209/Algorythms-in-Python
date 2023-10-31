from __future__ import annotations
from typing import Callable
import numpy as np

class Neuron:
    def __init__(self, activation_function: Callable[[float], float], 
                 derivative_activation_function: Callable[[float], float], 
                 weights: np.NDArray[float],
                 learning_rate: float):
        self.activation_function = activation_function
        self.derivative_activation_function = derivative_activation_function
        self.weights = weights
        self.output_cache: float = 0.0
        self.delta: float = 0.0
        self.learning_rate = learning_rate

    def output(self, inputs: np.NDArray[float]) -> float:
        """
        calculates the output of the neuron based on its weights.
        """
        output: float = np.dot(inputs, self.weights)
        self.output_cache = output
        return self.activation_function(output)
