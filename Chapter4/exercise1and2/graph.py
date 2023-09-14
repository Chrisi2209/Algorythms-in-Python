from __future__ import annotations
from typing import List, Tuple, TypeVar, Dict, Optional 
from dataclasses import dataclass
import sys
sys.path.insert(0, "C:\\Programmieren\\VS_Code\\pythonAlgorithmusÜbungen\\Chapter2")
from generic_search import bfs, Node, PriorityQueue

v = TypeVar("v")  # vertex (a string)

@dataclass
class Edge:
    f: int
    to: int
    
    def reverse(self):
        return Edge(self.to, self.f)
    

class Graph:
    def __init__(self, vertecies: List[v]):
        self._vertecies: List[v] = vertecies
        self._edges: List[List[Edge]] = []
        for vertex in self._vertecies:
            self._edges.append([])

    @property
    def edge_count_one_way(self):
        count = 0
        for i in range(len(self._edges)):
            for edge in self._edges[i]:
                count += 1

        return count
    
    @property
    def edge_count(self):
        """Only works if all edges are bidirectional"""
        count = 0
        for i in range(len(self._edges)):
            for edge in self._edges[i]:
                count += 1

        return count / 2

    def add_vertex(self, vertex: v) -> None:
        self._vertecies.append(vertex)
        self._edges.append([])

    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.f].append(edge)
        self._edges[edge.to].append(edge.reverse())

    def add_edge_by_indices(self, f: int, to: int) -> None:
        edge: Edge = Edge(f, to)
        self.add_edge(edge)

    def add_edge_by_vertexes(self, f: v, to: v) -> None:
        edge: Edge = Edge(self.index_from_vertex(f), self.index_from_vertex(to))
        self.add_edge(edge)

    def add_edge_oneway(self, edge: Edge) -> None:
        self._edges[edge.f].append(edge)

    def add_edge_by_indices_oneway(self, f: int, to: int) -> None:
        edge: Edge = Edge(f, to)
        self.add_edge_oneway(edge)

    def add_edge_by_vertexes_oneway(self, f: v, to: v) -> None:
        edge: Edge = Edge(self.index_from_vertex(f), self.index_from_vertex(to))
        self.add_edge_oneway(edge)

    def vertex_from_index(self, index: int) -> v:
        return self._vertecies[index]
    
    def index_from_vertex(self, vertex: v) -> int:
        return self._vertecies.index(vertex)

    def neighbours_for_vertex(self, index: int) -> List[int]:
        return [edge.to for edge in self._edges[index]]
    
    def copy(self) -> Graph:
        graph: Graph = Graph(self._vertecies)
        for edge_list in self._edges:
            for edge in edge_list:
                graph.add_edge_by_indices_oneway(edge.f, edge.to)

        return graph
    
    #### Excersice 1 #####
    def remove_vertex_index(self, index: int):
        self._vertecies.pop(index)
        self._edges.pop(index)
    
    def remove_vertex(self, vertex: v):
        index: int = self.index_from_vertex(vertex)
        self.remove_vertex_index(index)
    
    def remove_edge(self, edge: Edge):
        self._edges[edge.f].remove(edge)

    def remove_edge_f_to_oneway(self, f: int, to: int):
        for i, edge in enumerate(self._edges[f]):
            if edge.f == f and edge.to == to:
                self._edges[f].pop(i)
                break
    
    def remove_edge_f_to(self, f: int, to: int):
        self.remove_edge_f_to_oneway(f, to)
        self.remove_edge_f_to_oneway(to, f)

@dataclass
class WeightedEdge(Edge):
    weight: float
    def reverse(self) -> WeightedEdge:
        return WeightedEdge(self.to, self.f, self.weight)
    
    def __lt__(self, other: WeightedEdge):
        return self.weight < other.weight


class WeightedGraph(Graph):
    def __init__(self, vertecies: List[v]):
        self._vertecies: List[v] = vertecies
        self._edges: List[List[WeightedEdge]] = []
        for v in self._vertecies:
            self._edges.append([])

    def add_vertex(self, vertex: v) -> None:
        self._vertecies.append(vertex)
        self._edges.append([])

    def add_edge(self, edge: WeightedEdge) -> None:
        self._edges[edge.f].append(edge)
        self._edges[edge.to].append(edge.reverse())

    def add_edge_by_indices(self, f: int, to: int, weight: float) -> None:
        edge: WeightedEdge = WeightedEdge(f, to, weight)
        self.add_edge(edge)

    def add_edge_by_vertexes(self, f: v, to: v, weight: float) -> None:
        edge: WeightedEdge = WeightedEdge(self.index_from_vertex(f), self.index_from_vertex(to), weight)
        self.add_edge(edge)

    def add_edge_oneway(self, edge: WeightedEdge) -> None:
        self._edges[edge.f].append(edge)

    def add_edge_by_indices_oneway(self, f: int, to: int, weight: float) -> None:
        edge: WeightedEdge = WeightedEdge(f, to, weight)
        self.add_edge_oneway(edge)

    def add_edge_by_vertexes_oneway(self, f: v, to: v, weight: float) -> None:
        edge: WeightedEdge = WeightedEdge(self.index_from_vertex(f), self.index_from_vertex(to), weight)
        self.add_edge_oneway(edge)

    def vertex_from_index(self, index: int) -> v:
        return self._vertecies[index]
    
    def index_from_vertex(self, vertex: v) -> int:
        return self._vertecies.index(vertex)

    def neighbours_for_vertex(self, index: int) -> List[int]:
        return [edge.to for edge in self._edges[index]]
    
    
    def neighbours_and_weights_for_vertex(self, index: int) -> List[Tuple[int, float]]:
        return zip([edge.to for edge in self._edges[index]], [edge.weight for edge in self._edges[index]])
    
    @property
    def vertex_count(self):
        return len(self._vertecies)
    
    #### Excersice 1 #####
    def remove_vertex_index(self, index: int):
        self._vertecies.pop(index)
        self._edges.pop(index)
    
    def remove_vertex(self, vertex: v):
        index: int = self._vertecies.index(vertex)
        self.remove_vertex_index(index)
    
    def remove_edge(self, edge: WeightedEdge):
        for i, cur_edge in enumerate(self._edges[edge.f]):
            if cur_edge.to == edge.to:
                self._edges[edge.f].pop(i)


@dataclass
class DijkstraNode:
    vertex: int
    distance: float
    def __lt__(self, other: DijkstraNode):
        return self.distance < other.distance
    
    def __eq__(self, other: DijkstraNode):
        return self.distance == other.distance
    
def dijkstra(wg: WeightedGraph, root: v) -> Tuple(List[Optional[float]], Dict[int, int]):
    first: int = wg.index_from_vertex(root)
    distances: List[Optional[float]] = [None] * wg.vertex_count
    pathes: Dict[int, int] = {}
    search = PriorityQueue()
    search.push(DijkstraNode(first, 0))
    distances[first] = 0

    while not search.empty:
        current = search.pop().vertex
        neighbours_with_weights = wg.neighbours_and_weights_for_vertex(current)
        for neighbour, weight in neighbours_with_weights:
            if distances[neighbour] is None or distances[neighbour] > distances[current] + weight:
                distances[neighbour] = distances[current] + weight
                pathes[neighbour] = current

                search.push(DijkstraNode(neighbour, distances[neighbour]))
    
    return distances, pathes

def jarnik(wg: WeightedGraph, start: int = 0) -> Optional[List[WeightedEdge]]:
    pass
    # ....... See Kapitel 4 im Buch
        


class VertexRoute:
    def __init__(self, graph: Graph):
        self._route: List[int] = []
        self._graph: Graph = graph
    
    def set_route(self, route: List[int]):
        self._route = route

    def route_from_node(self, node: Node):
        self._route.clear()
        while node is not None:
            self.add_index(node.state)
            node = node.parent

        self._route = self._route[::-1]

    def add_index(self, index: int):
        self._route.append(index)
    
    def add_vertex(self, vertex: v):
        self._route.append(self._graph.index_from_vertex(vertex))
    
    def __repr__(self):
        return " -> ".join([self._graph.vertex_from_index(index) for index in self._route])
    

if __name__ == "__main__":
    graph: Graph = Graph(["Eisenstadt", "Marz", "Wien", "St. Pölten", "Linz", "Graz", "Klagenfurt", 
                          "Salzburg", "Innsbruck", "Bregenz", "Seebenstein", "Gleißenfeld", 
                          "Großglockner"])
    
    graph.add_edge_by_vertexes("Bregenz", "Innsbruck")
    graph.add_edge_by_vertexes("Innsbruck", "Salzburg")
    graph.add_edge_by_vertexes("Innsbruck", "Großglockner")
    graph.add_edge_by_vertexes("Großglockner", "Salzburg")
    graph.add_edge_by_vertexes("Salzburg", "Klagenfurt")
    graph.add_edge_by_vertexes("Salzburg", "Linz")
    graph.add_edge_by_vertexes("Linz", "Graz")
    graph.add_edge_by_vertexes("Linz", "St. Pölten")
    graph.add_edge_by_vertexes("Graz", "Klagenfurt")
    graph.add_edge_by_vertexes("St. Pölten", "Wien")
    graph.add_edge_by_vertexes("Graz", "St. Pölten")
    graph.add_edge_by_vertexes("St. Pölten", "Seebenstein")
    graph.add_edge_by_vertexes("Seebenstein", "Gleißenfeld")
    graph.add_edge_by_vertexes("Seebenstein", "Marz")
    graph.add_edge_by_vertexes("Seebenstein", "Wien")
    graph.add_edge_by_vertexes_oneway("Wien", "Eisenstadt")
    graph.add_edge_by_vertexes("Eisenstadt", "Marz")

    start: v = "Seebenstein"
    # goal: v = graph.index_from_vertex("Eisenstadt")
    # end_node: Node = bfs(graph.neighbours_for_vertex, lambda x: x == goal, graph.index_from_vertex(start))



    # route: VertexRoute = VertexRoute(graph)
    # route.route_from_node(end_node)
    # print(route)

    wg: WeightedGraph = WeightedGraph(["Eisenstadt", "Marz", "Wien", "St. Pölten", "Linz", "Graz", "Klagenfurt", 
                          "Salzburg", "Innsbruck", "Bregenz", "Seebenstein", "Gleißenfeld", 
                          "Großglockner"])
    
    wg.add_edge_by_vertexes("Bregenz", "Innsbruck", 50)
    wg.add_edge_by_vertexes("Innsbruck", "Salzburg", 60)
    wg.add_edge_by_vertexes("Innsbruck", "Großglockner", 40)
    wg.add_edge_by_vertexes("Großglockner", "Salzburg", 30)
    wg.add_edge_by_vertexes("Salzburg", "Klagenfurt", 150)
    wg.add_edge_by_vertexes("Salzburg", "Linz", 120)
    wg.add_edge_by_vertexes("Linz", "Graz", 250)
    wg.add_edge_by_vertexes("Linz", "St. Pölten", 100)
    wg.add_edge_by_vertexes("Graz", "Klagenfurt", 90)
    wg.add_edge_by_vertexes("St. Pölten", "Wien", 160)
    wg.add_edge_by_vertexes("Graz", "St. Pölten", 120)
    wg.add_edge_by_vertexes("St. Pölten", "Seebenstein", 160)
    wg.add_edge_by_vertexes("Seebenstein", "Gleißenfeld", 20)
    wg.add_edge_by_vertexes("Seebenstein", "Marz", 170)
    wg.add_edge_by_vertexes("Seebenstein", "Wien", 260)
    wg.add_edge_by_vertexes_oneway("Wien", "Eisenstadt", 300)
    wg.add_edge_by_vertexes("Eisenstadt", "Marz", 100)

    distances, path = dijkstra(wg, start)

    for vertex, distance in enumerate(distances):
        print(f"{wg.vertex_from_index(vertex)}: {distance}")

