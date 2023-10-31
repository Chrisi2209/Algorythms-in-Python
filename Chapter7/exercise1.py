import os
from typing import List, Dict, Tuple
from random import shuffle
from collections import defaultdict
import csv
import pprint

from util import normalize_by_feature_scaling, sigmoid, derivative_sigmoid
from network import Network


def read_adult() -> Tuple[List[List[float]], List[str], List[defaultdict[str, float]]]:
    """
    basically csv parser just that the different strings of a parameter are converted into an integer.
    """

    with open(os.path.realpath(os.path.join(os.path.abspath(__file__), "..", "data", "adult.csv")), "r") as f:
        lines: List[List[str]] = list(csv.reader(f))
        shuffle(lines)
        
        # for each parameter, get a defaultdict
        parameter_dict: List[defaultdict[str, float]] = [defaultdict(lambda i=i: float(len(parameter_dict[i]))) for i in range(len(lines[0]))]

        parameters: List[List[float]] = []

        for line in lines:
            data: List[float] = []
            for parameter_index, parameter_value in enumerate(line[:-1]):
                try:
                    data.append(float(parameter_value.strip()))
                except ValueError:
                    data.append(parameter_dict[parameter_index][parameter_value.strip()])
            
            parameters.append(data)
        
        labels: List[str] = [line[-1].strip() for line in lines]
    
    normalize_by_feature_scaling(parameters)
    
    return parameters, labels, parameter_dict


def test_adult():
    parameters, labels, parameter_dict = read_adult()
    network = Network([14, 8, 2], sigmoid, derivative_sigmoid, 0.3)  # sigmoid activation

    for _ in range(50):
        network.train(parameters[:1000], [adult_label_to_expected(label) for label in labels[:1000]])

    success, total, percentage = network.validate(parameters[1000:2000], labels[1000:2000], interpret_adult)

    print(f"{success} out of {total} jobs were successfully identified. ({percentage * 100}%)")


def adult_label_to_expected(label: str) -> List[float]:
    if label == ">50K":
        return [1, 0]
    
    if label == "<=50K":
        return [0, 1]
    
    else:
        raise Exception()


def interpret_adult(output: List[float]) -> str:
    if max(output) == output[0]:
        return ">50K"
    
    if max(output) == output[1]:
        return "<=50K"

    else:
        raise Exception()
    
def test_adult2():
    parameters, labels, parameter_dict = read_adult()
    network = Network([14, 8, 1], sigmoid, derivative_sigmoid, 0.3)  # sigmoid activation

    for _ in range(50):
        network.train(parameters[:-1000], [adult_label_to_expected2(label) for label in labels[:-1000]])

    success, total, percentage = network.validate(parameters[-1000:], labels[-1000:], interpret_adult2)

    print(f"{success} out of {total} jobs were successfully identified. ({percentage * 100}%)") # (86% mit aktueller Einstellung)


def adult_label_to_expected2(label: str) -> List[float]:
    if label == ">50K":
        return [1]
    
    if label == "<=50K":
        return [0]
    
    else:
        raise Exception()


def interpret_adult2(output: List[float]) -> str:
    if output[0] >= 0.5:
        return ">50K"
    
    else:
        return "<=50K"
    


if __name__ == "__main__":
    test_adult2()
