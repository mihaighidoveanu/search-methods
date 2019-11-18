from map import Map
from astar import AStar
import numpy as np
import heapq

class PathFinder(AStar):

    def __init__(self, graph, verbose = False):
        self.verbose = verbose
        self.graph = graph

    def neighbors(self, node):
        neighbors = self.graph[node]
        if self.verbose:
            print('N', node, neighbors)
        return neighbors

    def distance_between(self, n1, n2):
        dist =  np.linalg.norm(n1 - n2)
        if self.verbose:
            print('G ', n1, n2, dist)
        return dist

    def heuristic_cost_estimate(self, n1, n2):
        dist = np.linalg.norm(n1 - n2)
        if self.verbose:
            print('H ', n1, n2, dist)
        return dist

def best_first_search(graph, start, end):
    pq = [] # priority queue
    path = []
    visited = set() 
    heapq.heappush(pq, (0, start))
    while len(pq) != 0:
        _, point = heapq.heappop(pq)
        path.append(point)
        if point == end:
            print('Finished')
            return path
        else:
            for neighbor in graph[point]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    dist = np.linalg.norm( neighbor - end)
                    heapq.heappush(pq, (dist, neighbor))
    return path

def eval(path):
    d = 0
    for i in range(len(path) - 1):
        d += np.linalg.norm( path[i + 1] - path[i])
    return d

def run(fin):
    map = Map.from_file(fin)
    solver = PathFinder(map.graph)
    solution = solver.astar(map.start, map.end)
    if solution is not None:
        print(f'Shortest path from {map.start} to {map.end} :')
        path = list(solution)
        print(path)
        print('Cost ', eval(path))
    else:
        print('No solution found')
    path = best_first_search(map.graph, map.start, map.end)
    print(path)
    print('Cost ', eval(path))

import fire
if __name__ == '__main__':
    fire.Fire(run)
