import os
import collections

Point = collections.namedtuple('Point', ['y', 'x'])

def int_readline(f):
    return [int(number) for number in next(f).split()]

class Coords:
    @staticmethod
    def north():
        return Point(-1,0)

    @staticmethod 
    def south():
        return Point(1,0)

    @staticmethod 
    def east():
        return Point(0,1)

    @staticmethod  
    def west():
        return Point(0,-1)

    @staticmethod   
    def list():
        return [Coords.north(), Coords.south(), Coords.east(), Coords.west()]
	
class State:
    def __init__(self, point, orientation):
        self.point = point
        self.orientation = orientation

    def next(self, orientation = None):
        if orientation is None:
            orientation = self.orientation
        new_point = Point(self.point.y + orientation.y, self.point.x + orientation.x)
        return State(new_point, orientation)

    def neighbours(self):
        nexts_or = Coords.list()
        nexts_or.remove(self.orientation)
        nexts = [self.next(orientation) for orientation in nexts_or]
        return nexts

    def __str__(self):
        return f'{self.point}--->{self.orientation}'

    def __repr__(self):
        return str(self)

class Maze:
    def __init__(self, matrix, start, end):
        assert(type(matrix is list))
        assert(type(matrix[0]) is list)
        assert(type(start) is Point and type(end) is Point)
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.start = State(start, Coords.north())
        self.end = end

    def __getitem__(self, point):
        i, j = point
        if i >= self.rows or i < 0 :
            return None
        if j >= self.cols or j < 0 :
            return None
        return self.matrix[i][j]

    def __setitem__(self, point, value):
        i, j = point
        if i >= self.rows or i < 0 :
            return 
        if j >= self.cols or j < 0 :
            return 
        self.matrix[i][j] = value

    def is_finish(self, point):
        return point == self.end 

    def can_visit(self, point):
        return self[point] == 0

    def visit(self, point):
        self[point] = 2

    @staticmethod
    def read_matrix(fname):
        matrix = []
        with open(fname, 'r') as f:
            rows = int_readline(f)[0]
            start = Point(*int_readline(f))
            end = Point(*int_readline(f))
            for _ in range(rows):
                values = int_readline(f)
                matrix.append(values)
        
        maze = Maze(matrix, start, end)
        return maze

import copy
if __name__ == '__main__':
    fin = 'input_maze.txt'
    maze = Maze.read_matrix(fin) 

