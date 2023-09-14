from typing import Set, Tuple, Optional, Dict, List

import sys
sys.path.append('C:\\Programmieren\\VS_Code\\pythonAlgorithmusÜbungen\\Chapter4\\')

from excersice1and2 import graph

def traverse_each_edge(graph: graph.Graph, position: int=0) -> Optional[bool]:
    if graph.edge_count == 0:
        return [position]
    

    for neighbour in graph.neighbours_for_vertex(position):
        graph_copy: graph.Graph = graph.copy()

        graph_copy.remove_edge_f_to(position, neighbour)
        
        result: Optional[List[int]] = traverse_each_edge(graph_copy, neighbour)

        if result is None:
            continue

        result.append(neighbour)
        return result

    # wenn keine Lösung für dieses Assignment gefunden wurde
    return None


if __name__ == "__main__":
    königsberg: graph.Graph = graph.Graph(["Left", "Top", "Right", "Bottom"])

    königsberg.add_edge_by_vertexes("Left", "Top")
    königsberg.add_edge_by_vertexes("Left", "Top")
    
    königsberg.add_edge_by_vertexes("Left", "Bottom")
    königsberg.add_edge_by_vertexes("Left", "Bottom")

    königsberg.add_edge_by_vertexes("Right", "Top")
    königsberg.add_edge_by_vertexes("Right", "Bottom")

    
    königsberg.add_edge_by_vertexes("Left", "Right")

    result: Optional[List[int]] = traverse_each_edge(königsberg)
    if result is None:
        print("No solution found!")
    else:
        print("Left -> " + " -> ".join([königsberg.vertex_from_index(n) for n in result[::-1]]))

    



    

