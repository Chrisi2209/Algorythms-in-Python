"""
imports a csv file provided by a command line argument
and creates DataPoint objects with the data.
Accepted format:
first item contains one number. This is the dimension n.
From the next line on, each line is treated as one Datapoint.
"""

import os
import sys
import csv
from typing import List

sys.path.insert(0, os.path.realpath(os.path.join(os.path.realpath(__file__), "..", "..")))

from data_point import DataPoint

def import_data_points_csv(path: str):
    data_points: List[DataPoint] = []
    # get csv
    with open(path, "r", newline="") as f:
        reader: csv._reader = csv.reader(f)

        # get dimension
        try:
            dimension = int(next(reader)[0])
        except TypeError:
            print("The dimension could not be resolved.")
            return None

        # read rows
        for row in reader:
            if len(row) != dimension:
                print(f"error: dimension of row is not {dimension}. Values: {row}")
                return None
            
            dimensions: List[float] = []
            for i in range(dimension):
                dimensions.append(float(row[i]))

            data_points.append(DataPoint(dimensions))
    
    return data_points


if __name__ == "__main__":
    path = os.path.realpath(os.path.join(os.path.realpath(__file__), "..", "data.csv"))
    if len(sys.argv) == 2:
        path = os.path.abspath(sys.argv[1])
    
    print("\n".join(map(str, import_data_points_csv(path))))