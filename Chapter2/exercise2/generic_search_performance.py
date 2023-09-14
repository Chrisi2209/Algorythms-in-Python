import sys
sys.path.append('C:\\Programmieren\\VS_Code\\pythonAlgorithmusÜbungen\\Chapter2\\')

from typing import Iterable
import generic_search

def sum(array: Iterable[int]):
    summ = 0
    for element in array:
        summ += element

    return summ


if __name__ == "__main__":
    counts_dfs = []
    counts_bfs = []
    counts_astar = []
    for _ in range(1_000):
        maze: generic_search.Maze = generic_search.Maze(rows=50, columns=50, start=generic_search.MazeLocation(49, 49))

        if (count:=generic_search.count_dfs(maze.successors, maze.goal_test, maze.start))[0] is not None:
            counts_dfs.append(count[1])
        if (count:=generic_search.count_bfs(maze.successors, maze.goal_test, maze.start))[0] is not None:
            counts_bfs.append(count[1])
        if (count:=generic_search.count_astar(maze.successors, maze.goal_test, maze.start, 
                            generic_search.manhattan_distance(maze.goal)))[0] is not None:
            counts_astar.append(count[1])

    print("dfs results:")
    print(counts_dfs)

    print("bfs results:")
    print(counts_bfs)

    print("astar results:")
    print(counts_astar)

    print("averages:")
    print(f"dfs:   {sum(counts_dfs) / 1000}")
    print(f"bfs:   {sum(counts_bfs) / 1000}")
    print(f"astar: {sum(counts_astar) / 1000}")

