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
    visited = set() 
    heapq.heappush(pq, (0, start))
    while len(pq) != 0:
        _, point = heapq.heappop(pq)
        print(point)
        if point == end:
            print('Finished')
            return None
        else:
            for neighbor in graph[point]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    dist = np.linalg.norm( neighbor - end)
                    heapq.heappush(pq, (dist, neighbor))
    print('Not found')

    


if __name__ == '__main__':
    fin = 'input.txt'
    map = Map.from_file(fin)
    solver = PathFinder(map.graph)
    solution = solver.astar(map.start, map.end)
    if solution is not None:
        print(f'Shortest path from {map.start} to {map.end} :')
        print(list(solution))
    else:
        print('No solution found')
    best_first_search(map.graph, map.start, map.end)
