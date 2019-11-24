import os
import collections
import copy

def dfs(maze, state):
    maze = copy.deepcopy(maze)
    stack = [state]
    path = [state]

    while len(stack) != 0 :
        state = stack.pop(-1) 
        point = state.point

        while maze.can_visit(point):
            # print('Forward ', point, maze[point], state.orientation)
            if maze.is_finish(point):
                print('FINISH')
                print('Traversed matrix')
                for row in maze.matrix:
                    for val in row:
                        print(f'{val:d}   ', end = '')
                    print()
                return point 
            maze.visit(point)
            neighbours = state.neighbours()
            # print('Neighbors', neighbours)
            for  nstate in neighbours:
                if maze.can_visit(nstate.point):
                    # print('Add Neighbour ', nstate)
                    stack.append(nstate)
            state = state.next()
            point = state.point


def bfs():
    maze = copy.deepcopy(maze)
    queue = [state]
    path = [state]

    while len(queue) != 0 :
        state = queue.pop(0)
        point = state.point

        if maze.is_finish(point):
            print('FINISH')
            print('Traversed matrix')
            for row in maze.matrix:
                for val in row:
                    print(f'{val:d}   ', end = '')
                print()
            return point 
        maze.visit(point)
        neighbours = state.neighbours()
        # print('Neighbors', neighbours)
        for  nstate in neighbours:
            if maze.can_visit(nstate.point):
                # print('Add Neighbour ', nstate)
                queue.append(nstate)

from maze import Maze, State

if __name__ == '__main__':
    fin = 'input_maze.txt'
    maze = Maze.read_matrix(fin) 

    for row in maze.matrix:
        print(row)

    print('The end should be ', maze.end)

    print('dfs ', dfs(maze, maze.start))

