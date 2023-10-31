from __future__ import annotations
from typing import Callable, List, TypeVar, Tuple
from random import random
from functools import reduce
import numpy as np

from layer import Layer

T = TypeVar("T")

class Network:
    def __init__(self, structure: List[int], 
                 activation_function: Callable[[float], float], 
                 derivative_activation_function: Callable[[float], float],
                 learning_rate: float):
        
        if len(structure) < 3:
            raise Exception("len of structure > 2 (1 input, 1 hidden, 1 output layer)")

        self.structure = structure
        self.activation_fuction = activation_function
        self.derivative_activation_function = derivative_activation_function
        
        self.layers: List[Layer] = [Layer(self.structure[0], None, self.activation_fuction, self.derivative_activation_function, learning_rate),]

        for previous, num_neurons in enumerate(structure[1:]):
            self.layers.append(Layer(num_neurons, self.layers[previous], self.activation_fuction, self.derivative_activation_function, learning_rate))


    def outputs(self, input: np.NDArray[float]) -> List[float]:
        """
        calculate the output for a given input
        """
        return reduce(lambda inputs, layer: layer.output(inputs), self.layers, input)
    
    def backpropagate(self, expected: np.NDArray[float]):
        """
        calculates deltas for each layer
        Uses the following formula for hidden layers: delta = f'(output_cache) * dot(deltas_of_next_neurons, weights_of_next_neurons_for_this_neuron)
        """
        last_layer = len(self.layers) - 1

        self.layers[last_layer].calculate_delta_for_output_layer(expected)

        # first layer does not have weights and therefore also don't have a delta
        for layer in range(last_layer - 1, 0, -1):
            self.layers[layer].calculate_delta_for_hidden_layer(self.layers[layer + 1])

    def update_weights(self):
        """
        assigns the new weights after the deltas were calculated by backpropagate.
        Uses the following formula: new_weight = old_weight + (learning_rate * delta * output_where_wheight_is_inflicted)
        """
        for layer in self.layers:
            for neuron in layer.neurons:
                for w in range(len(neuron.weights)):
                    neuron.weights[w] = neuron.weights[w] + (neuron.learning_rate * neuron.delta * layer.previous_layer.output_cache[w])

    def train(self, inputs: List[np.NDArray[float]], expecteds: List[List[float]]) -> None:
        for input, expected in zip(inputs, expecteds):
            outputs: List[float] = self.outputs(input)
            self.backpropagate(expected)
            self.update_weights()


    def validate(self, inputs: List[np.NDArray[float]], expecteds: List[T], interpret_output: Callable[[List[float]], T]) -> Tuple[int, int, float]:
        """
        runs the network for the input and then checks how many are correct. 
        The result is interpreted first before checked if its the same as expected
        """
        correct: int = 0
        for input, expected in zip(inputs, expecteds):
            result: T = interpret_output(self.outputs(input))
            if result == expected:
                correct += 1
        
        percentage: float = correct / len(inputs)
        return correct, len(inputs), percentage
