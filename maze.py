import os
import collections



# class Point(object):

#     def __init__(self, y, x, is_start = False, is_end = False):
#         self.x = x
#         self.y = y
#         if is_start or is_end:
#             assert(is_start != is_end)
#         self.is_start = is_start
#         self.is_end = is_end
    
Point = collections.namedtuple('Point', ['x', 'y'])

def int_readline(f):
    return [int(number) for number in next(f).split()]

class Maze:

    def __init__(self, matrix, start, end):
        assert(type(matrix is list))
        assert(type(matrix[0]) is list)
        assert(type(start) is Point and type(end) is Point)
        self.matrix = matrix
        self.start = start
        self.end = end

    @staticmethod
    def _read_graph(fname):
        pass

    @staticmethod
    def _read_matrix(fname):
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

    @staticmethod
    def from_file(fname, graph_format = False):
        if graph_format:
            return Maze._read_graph(fname)
        else:
            return Maze._read_matrix(fname)

    def _is_intersectionPoint(self, row, col):
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        points_on_col = [self.matrix[i][col] for i in [row + 1, row - 1]  if i in range(rows) ]
        points_on_row = [self.matrix[row][j] for j in [col + 1, col - 1] if j in range(cols) ]
        intersections = [ (p1 == 0 and p1 == p2) for p1 in points_on_col for p2 in points_on_row]
        is_intersection = sum(intersections) >= 1
        return is_intersection 

    def to_graph(self):
        graph = collections.defaultdict(list)
        rows_size = len(self.matrix)
        cols_size = len(self.matrix[0])
        # store last point encountered for each row and column
        prev_on_col = [None] * cols_size  
        prev_on_row = [None] *  rows_size 
        for i, row in enumerate(self.matrix):
            for j, val in enumerate(row):
                if val == 0 :
                    if self._is_intersectionPoint(i, j):
                        new_point = Point(i,j)
                        # previous col index on row j
                        prev_ci = prev_on_row[i] 
                        if prev_ci is not None:
                            old_point = Point(i, prev_ci)
                            graph[old_point].append(new_point)
                            graph[new_point].append(old_point)
                        # previous row index on col i
                        prev_ri = prev_on_col[j] 
                        if prev_ri is not None:
                            old_point = Point(prev_ri, j)
                            graph[old_point].append(new_point)
                            graph[new_point].append(old_point)
                        # update intersections
                        prev_on_col[j] = i
                        prev_on_row[i] = j
                elif val == 1 :
                    prev_on_col[j] = None
                    prev_on_row[i] = None                    

        return graph

if __name__ == '__main__':
    fin = 'input_maze.txt'
    maze = Maze.from_file(fin)
    graph = maze.to_graph()
    for key in graph.keys():
        print( key, ' : ', graph[key])


