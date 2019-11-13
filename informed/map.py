import os
import collections

BasePoint = collections.namedtuple('BasePoint', ['x', 'y'])
class Point(BasePoint):
    @staticmethod
    def from_str(str):
        return Point(*[int(coord) for coord in str.split()])


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

    def __repr__(self):
        return repr([repr(point) for point in self.points])


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


    @staticmethod
    def from_file(path):
        with open(path, 'r') as file:
            start = Point.from_str(next(file))
            end = Point.from_str(next(file))
            polyes = []
            for line in file:
                polyes.append(Poly.from_str(line))
        return Map(start, end, polyes) 


if __name__ == '__main__':
    fin = 'input.txt'
    map = Map.from_file(fin)
    print(map.start)
    print(map.end)
    print(map.polygons)
