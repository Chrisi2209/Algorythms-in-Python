from __future__ import annotations
from typing import Callable, List, Optional
from random import random
import numpy as np

from neuron import Neuron


class Layer:
    def __init__(self, num_neurons: int, previous_layer: Optional[Layer],
                 activation_function: Callable[[float], float], 
                 derivative_activation_function: Callable[[float], float],
                 learning_rate: float):

        self.previous_layer = previous_layer
        self.activation_function = activation_function
        self.derivative_activation_function = derivative_activation_function
        self.output_cache: List[float] = [0.0 for _ in range(num_neurons)]

        self.neurons: List[Neuron] = []
        for _ in range(num_neurons):
            if self.previous_layer is None:
                self.neurons.append(Neuron(self.activation_function, self.derivative_activation_function, [], learning_rate))
            else:
                weights: int = [random() for _ in range(len(previous_layer.neurons))]
                self.neurons.append(
                    Neuron(self.activation_function, self.derivative_activation_function, weights, learning_rate)
                )


    def output(self, inputs: np.NDArray[float]) -> List[float]:
        """
        gets an input to the layer and the output is determined by each neurons weights
        """
        if self.previous_layer is None:
            self.output_cache = inputs
            
        else:
            self.output_cache = [n.output(inputs) for n in self.neurons]

        return self.output_cache
    
    def calculate_delta_for_output_layer(self, expected: np.NDArray[float]):
        """
        should only be called upon a output layer. Gets the expected output and calculates the deltas for the neurons
        """
        for n in range(len(self.neurons)):
            self.neurons[n].delta = self.neurons[n].derivative_activation_function(self.neurons[n].output_cache) * (expected[n] - self.output_cache[n])


    def calculate_delta_for_hidden_layer(self, next_layer: Layer):
        """
        calculates the deltas for a hidden layer-
        It uses following formula: delta = f'(output_cache) * dot(weights_for_this_neuron_of_next_layer, deltas_of_next_layer)
        """
        for index, neuron in enumerate(self.neurons):
            next_weights: np.NDArray[float] = np.array([n.weights[index] for n in next_layer.neurons])
            next_deltas: np.NDArray[float] = np.array([n.delta for n in next_layer.neurons])

            temp: float = np.dot(next_weights, next_deltas)

            neuron.delta = neuron.derivative_activation_function(neuron.output_cache) * temp

