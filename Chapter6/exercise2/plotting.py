import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
from typing import List
from collections import defaultdict

sys.path.insert(0, os.path.realpath(os.path.join(os.path.realpath(__file__), "..", "..")))

from k_means import KMeans
from data_point import DataPoint

def plot_clusters(clusters: List[KMeans.Cluster]):
    dimensions: int = clusters[0].centroid.num_dimensions
    all_points: List[DataPoint] = []   
    color_mapping = defaultdict(lambda: "gray", {
            0: "red",
            1: "green",
            2: "blue",
            3: "yellow",
            4: "purple",
            5: "white",
            6: "black",
        })
    colors: List[int] = []

    for i, cluster in enumerate(clusters):
        all_points.extend(cluster.points)
        colors.extend(color_mapping[i] for _ in cluster.points)


    if dimensions == 1:
        x: List[float] = KMeans.dimension_slice(KMeans, 0, all_points)
        plt.scatter(x, [0 for _ in x], c=colors, label='Data Points')
        plt.show()

    elif dimensions == 2:
        x: List[float] = KMeans.dimension_slice(KMeans, 0, all_points)
        y: List[float] = KMeans.dimension_slice(KMeans, 1, all_points)

        plt.scatter(x, y, c=colors, label='Data Points')
        plt.show()

    elif dimensions == 3:
        x: List[float] = KMeans.dimension_slice(KMeans, 0, all_points)
        y: List[float] = KMeans.dimension_slice(KMeans, 1, all_points)
        z: List[float] = KMeans.dimension_slice(KMeans, 2, all_points)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(x, y, z, c=colors, marker='o', label='Data Points')
        plt.show()

    else:
        print("cannot plot more than 3D!")

