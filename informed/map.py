import os
import collections
import numpy as np
import itertools

BasePoint = collections.namedtuple('BasePoint', ['x', 'y'])
class Point(BasePoint):
    @staticmethod
    def from_str(str):
        return Point(*[int(coord) for coord in str.split()])

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def cross(self, other):
        prod = self.x * other. y - other.x * self.y
        return prod       

class Poly:
    def __init__(self, points):
        tp = type(points)
        assert (tp is list or tp is tuple)
        self.points = points

    @staticmethod
    def from_str(str):
        points = [(int(coord) for coord in coordinates.split('.')) for coordinates in str.split()]
        points = [Point(*coordinates) for coordinates in points]
        poly = Poly(points)
        return poly

    def __contains__(self, line):
        for i, point in enumerate(self.points):
            next_idx = (i + 1) % len(self.points)
            lineToCheck = [point, self.points[next_idx]]
            if line == lineToCheck:
                return True

    def __repr__(self):
        return repr([repr(point) for point in self.points])

    def __iter__(self):
        for i, point in enumerate(self.points):
            next_idx = (i + 1) % len(self.points)
            line = [point, self.points[next_idx]]
            yield line 


def onLine(point, line):
    # checks if point is on a sorted line segment
    line = sorted(line)
    cond = (line[0].x < point.x and point.x < line[1].x) and \
        (line[0].y < point.y and point.y < line[1].y)
    return cond
  
def orient(p, q, r):
    # checks orientation of three points
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # colinear 
    return 1 if val > 0 else 2 
  
def intersect(l1, l2):
    p1, q1 = l1
    p2, q2 = l2

    if p1 in l2 or q1 in l2:
        return False

    o1 = orient(p1, q1, p2); 
    o2 = orient(p1, q1, q2); 
    o3 = orient(p2, q2, p1); 
    o4 = orient(p2, q2, q1); 

    if o1 != o2 and o3 != o4:
        return True

    cond = ((o1 == 0) and onLine(p2, [p1, q1])) or \
        (o2 == 0 and onLine(q2, [p1, q1])) or \
        (o3 == 0 and onLine(p1, [p2, q2])) or \
        (o4 == 0 and onLine(q1, [p2, q2]))

    return cond

class Map:
    def __init__(self, start, end, polygons):
        tp = type(polygons)
        assert(tp is list or tp is tuple)
        if len(polygons) != 0:
            assert(type(polygons[0]) is Poly)
        ts = type(start)
        assert(ts is Point)
        te = type(end)
        assert(te is Point)
        self.polygons = polygons
        self.start = start
        self.end = end
        self._graph = None
        self._lines = None


    @staticmethod
    def from_file(path):
        with open(path, 'r') as file:
            start = Point.from_str(next(file))
            end = Point.from_str(next(file))
            polyes = []
            for line in file:
                polyes.append(Poly.from_str(line))
        return Map(start, end, polyes) 

    @property
    def lines(self):
        if self._lines is not None:
            return self._lines
        else:
            _lines = []
            for poly in self.polygons:
                for line in poly:
                    _lines.append(line)
            self._lines = _lines
            return self._lines

    def __contains__(self, line):
        return line in self.lines

    @property
    def graph(self):
        if self._graph is not None:
            return self._graph
        else:
            _graph = collections.defaultdict(list)
            all_points = [point for poly in self.polygons for point in poly.points]
            all_lines = []
            for i in range(len(all_points)):
                for j in range(i + 1, len(all_points)):
                    all_lines.append([all_points[i], all_points[j]])

            # add neighbors for the polyes vertices
            for l1 in all_lines:
                reachable = True
                for l2 in self.lines:
                    if l1 != l2:
                        if intersect(l1, l2):
                            reachable = False
                            break
                if reachable:
                    p, q = l1
                    _graph[p].append(q)
                    _graph[q].append(p)
            
            # add neighbors to start and end points
            for sp in [self.start, self.end]:
                for ep in all_points:
                    if sp == ep:
                        break
                    reachable = True
                    current_line = [sp, ep]
                    for line in self.lines:
                        if intersect(current_line, line):
                            reachable = False
                            break
                    if reachable:
                        _graph[sp].append(ep)
                        _graph[ep].append(sp)


            
            self._graph = _graph
            return self._graph
            


if __name__ == '__main__':
    fin = 'input.txt'
    map = Map.from_file(fin)
    for k,v in map.graph.items():
        print('Key ', k)
        print('Neighbors', v)
