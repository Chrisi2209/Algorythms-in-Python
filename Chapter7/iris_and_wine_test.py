from exercise2 import parse_csv
import os
from typing import List

from network import Network
from util import sigmoid, derivative_sigmoid, binary_step, binary_step_derivative, linear, linear_derivative


def test_iris():
    parameters, labels = parse_csv(os.path.realpath(os.path.join(os.path.abspath(__file__), "..", "data", "iris.csv")), False)
    # network = Network([4, 6, 3], sigmoid, derivative_sigmoid, 0.3)  # sigmoid activation
    network = Network([4, 6, 3], linear, linear_derivative, 0.3)  # linear activation

    for _ in range(50):
        network.train(parameters[:140], [iris_label_to_expected(label) for label in labels[:140]])

    success, total, percentage = network.validate(parameters[140:], labels[140:], interpret_iris)

    print(f"{success} out of {total} irises were successfully identified. ({percentage * 100}%)")


def iris_label_to_expected(label: str) -> List[float]:
    if label == "Iris-setosa":
        return [1, 0, 0]
    
    if label == "Iris-versicolor":
        return [0, 1, 0]
    
    if label == "Iris-virginica":
        return [0, 0, 1]


def interpret_iris(output: List[float]) -> str:
    if max(output) == output[0]:
        return "Iris-setosa"
    
    if max(output) == output[1]:
        return "Iris-versicolor"
    
    if max(output) == output[2]:
        return "Iris-virginica"

    else:
        raise Exception()


def test_wine():
    parameters, labels = parse_csv(os.path.realpath(os.path.join(os.path.abspath(__file__), "..", "data", "wine.csv")), True)
    #network = Network([13, 7, 3], sigmoid, derivative_sigmoid, 0.9)  # sigmoid activation
    network = Network([13, 7, 3], linear, linear_derivative, 0.9)  # linear activation
    
    for _ in range(10):
        network.train(parameters[:150], [wine_label_to_expected(label) for label in labels[:150]])

    success, total, percentage = network.validate(parameters[150:], labels[150:], interpret_wine)
    print(f"{success} out of {total} wines were successfully identified. ({percentage * 100}%)")


def wine_label_to_expected(label: str) -> List[float]:
    if label == "1":
        return [1, 0, 0]
    
    if label == "2":
        return [0, 1, 0]
    
    if label == "3":
        return [0, 0, 1]

    else:
        raise Exception()


def interpret_wine(output: List[float]) -> str:
    if max(output) == output[0]:
        return "1"
    
    if max(output) == output[1]:
        return "2"
    
    if max(output) == output[2]:
        return "3"

    else:
        raise Exception()

if __name__ == "__main__":
    test_iris()    
