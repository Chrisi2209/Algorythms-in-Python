"""
2023-09-14 Rodax Christopher

Program for K-Means Clustering
To use, create an instance of the KMeans class with
some data points. Set k to the number of clusters
that should be generated. After executing the run
method you receive the clusters that were found.
These have to do with an RNG so be sure to execute
it more than once.
"""

from __future__ import annotations
from functools import partial
from typing import List, Iterable, TypeVar, Optional
from statistics import pstdev, mean
from dataclasses import dataclass
from random import uniform, choice, choices
from copy import deepcopy
import os

from data_point import DataPoint

Point = TypeVar("Point", bound=DataPoint)

def zscore(dimension_values: Iterable[float]):
    """
    function to get normalized values for a certain
    dimension. This ensures that every dimension is weighted
    equally. Otherwise an axis with high differences are preferred
    over the others.
    """
    median: float = mean(dimension_values)
    stdev: float = pstdev(dimension_values)

    if stdev == 0:
        return [0] * len(dimension_values)

    return [(x - median) / stdev for x in dimension_values]

class KMeans:
    """
    Class for making a clustering of data points.
    Create an instance and run to cluster your data.
    """
    @dataclass
    class Cluster:
        """
        Sub class for storing clusters.
        """
        centroid: Point
        points: Point

    def __init__(self, points: Iterable[Point], k: int = 2, max_iterations=100) -> None:
        if len(points) == 0:
            raise AttributeError("at least one point per KMeans")

        # initialize properties
        self.points = points
        self.k = k
        self._max_iterations = max_iterations

        # normalize points
        self._normalize_points()

        # make clusters
        self._clusters: List[KMeans.Cluster] = []
        for _ in range(k):
            point: DataPoint = self._random_point()
            cluster: KMeans.Cluster = KMeans.Cluster(point, [])
            self._clusters.append(cluster)
            
    @property
    def num_dimensions(self):
        """ short hand for self.points[0].num_dimensions """
        return self.points[0].num_dimensions
    
    @property
    def _centroids(self):
        """ instantly get the centroid of each cluster """
        return [cluster.centroid for cluster in self._clusters]
    
    def run(self) -> List[KMeans.Cluster]:
        """Run this to cluster the data. The resulting clusters are returned."""
        for iteration in range(self._max_iterations):
            # clear all cluster points because the assing_clusters method 
            # only appends points and doesn't clear the old ones
            for cluster in self._clusters:
                cluster.points.clear()

            # figure out which points belong to which cluster in this iteration
            self._assign_clusters()

            # store the old centroids to know when the clusters converge
            old_centroids: List[Point] = deepcopy(self._centroids)

            # recalculate the centroids depending on the points assigned to them
            self._generate_centroids()

            # if no change on the centroids happened, it converged
            if old_centroids == self._centroids:
                print(f"Convergence after {iteration} iterations")
                return self._clusters
            
        return self._clusters

            

    def dimension_slice(self, dim: int, points: Optional[Iterable[Point]] = None) -> List[float]:
        """
        return the value of that dimension for each point of the KMeans if points = None
        else, only for the points that were inputtet
        """

        if points is None:
            points = self.points
        
        return [x.dimensions[dim] for x in points]
    
    def _normalize_points(self) -> None:
        """
        normalize, so that each axis is the same in terms of differences.
        """
        zscored: List[List[float]] = [[] for _ in range(len(self.points))]

        for dim in range(self.num_dimensions):
            # calculate zscores
            dim_scored = zscore(self.dimension_slice(dim))

            for index, score in enumerate(dim_scored):
                zscored[index].append(score)
        
        # assin the zscores to the points
        for index, point in enumerate(self.points):
            point.dimensions = tuple(zscored[index])
    
    def _random_point(self) -> Point:
        """
        get a random point inside the n-dimensional cube with the boundries of self.points
        """
        dimensions: List[float] = []
        for dim in range(self.num_dimensions):
            dim_slice = self.dimension_slice(dim)
            dimensions.append(uniform(min(dim_slice), max(dim_slice)))

        return DataPoint(dimensions)
    
    def _assign_clusters(self):
        """
        assign each point to the cluster that is nearest to them
        """
        for point in self.points:
            cluster = min(self._centroids, key=partial(DataPoint.distance, point))
            index = self._centroids.index(cluster)
            self._clusters[index].points.append(point)

    def _generate_centroids(self):
        """
        move the centroids to the mean of all its assigned points
        """
        for cluster in self._clusters:
            if len(cluster.points) == 0:
                continue

            means: List[float] = []
            
            for dim in range(self.num_dimensions):
                means.append(mean(self.dimension_slice(dim, cluster.points)))
            
            cluster.centroid = DataPoint(means)

    def define_centroids(self, centroids: List[Point]):
        if self.k != len(centroids):
            raise AttributeError("please specify the right amount of centroids")
        
        for cluster, new_centroid in zip(self._clusters, centroids):
            cluster.centroid = new_centroid
    
    def plus_plus(self):
        """
        call this method after initialization to use the kmeans++
        algorithm for determining where the clusters' starting positions
        are initialized
        """
        self._clusters.clear()

        first_centroid = deepcopy(choice(self.points))
        self._clusters.append(KMeans.Cluster(deepcopy(first_centroid), []))

        for i in range(self.k):
            distances: List[float] = []
            probabilities: List[float] = []
            # calculate probabilities
            for point in self.points:
                min_distance = float(min(map(partial(DataPoint.distance, point), self._centroids)))
                distances.append(min_distance ** 2)
            
            sum_of_distances = float(sum(distances))

            for distance in distances:
                probabilities.append(distance / sum_of_distances)
            
            # select by roulette
            point: Point = choices(self.points, probabilities, k=1)[0]
            self._clusters.append(KMeans.Cluster(deepcopy(point), []))
                




if __name__ == "__main__":
    # test
    """
    test_points = [
        DataPoint([2.0, 1.0, 1.0]),
        DataPoint([2.0, 2.0, 5.0]),
        DataPoint([3.0, 1.5, 2.5]),
    ]"""
    test_points = [
        DataPoint([2.0, 1.0]),
        DataPoint([2.0, 2.0]),
        DataPoint([3.0, 1.5]),
    ]
    for i in range(1):
        # k_means: KMeans = KMeans(test_points, k=2)
        # clusters: List[KMeans.Cluster] = k_means.run()

        # for i, cluster in enumerate(clusters):
        #     print(f"cluster {i}: {cluster.points}, centroid: {cluster.centroid}")
        
        from exercise2.plotting import plot_clusters
        # plot_clusters(clusters)

        from exercise1.csv_import import import_data_points_csv
        # print(os.path.realpath(os.path.join(os.path.realpath(__file__), "..", "exersice1", "data.csv")))

        for _ in range(100):
            k_means: KMeans = KMeans(import_data_points_csv(os.path.realpath(os.path.join(os.path.realpath(__file__), "..", "exercise1", "data2.csv"))), k=2)
            k_means.plus_plus()
            clusters = k_means.run()

            for i, cluster in enumerate(clusters):
                print(f"cluster {i}: {cluster.points}, centroid: {cluster.centroid}")
                
            plot_clusters(clusters)

