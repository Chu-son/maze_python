#-*- coding:utf-8 -*-
import numpy as np
import copy
import time

class Maze():
    def __init__(self, field_size):
        self.field_size = field_size

        self.maze_field = [ [ 1 for _ in range(field_size[0]) ] for _ in range(field_size[1])]
        self.directions = np.array([
                                    [1,0],
                                    [-1,0],
                                    [0,1],
                                    [0,-1]
                                    ])

        self.draw_char = ['　', '■', 'Ｓ', 'Ｇ', '＠']
        self.depth = 0
        self.max_depth = 0

    def create_maze(self, start_pos, goal_pos = None):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self._dig(start_pos)

        self.maze_field[start_pos[0]][start_pos[1]] = 2
        self.maze_field[self.goal_pos[0]][self.goal_pos[1]] = 3

        return self.maze_field

    def _dig(self, pos):
        self.depth += 1
        d = self.directions[np.random.permutation(self.directions.shape[0])]
        self.maze_field[pos[0]][pos[1]] = 0
        if self.goal_pos != None and pos[0] == self.goal_pos[0] and pos[1] == self.goal_pos[1]:return
        for dx,dy in d:
            if self._is_wall([pos[0]+dx*2,pos[1]+dy*2]):
                self.maze_field[pos[0] + dx][pos[1] + dy] = 0
                self._dig([pos[0]+dx*2,pos[1]+dy*2])
        if self.depth >= self.max_depth:
            self.max_depth = self.depth
            self.goal_pos = pos
        self.depth -= 1

    def _is_wall(self, pos):
        if self._is_out(pos) or self.maze_field[pos[0]][pos[1]] != 1:return False
        else:return True

    def _is_out(self, pos):
        if pos[0] >= self.field_size[0] or pos[0] < 0 \
                or pos[1] >= self.field_size[1] or pos[1] < 0:

            return True
        else: return False

    def print_maze(self, field = None):
        field = self.maze_field if field == None else field
        for row in field:
            for val in row:
                print(self.draw_char[val], end = '')
            print()
        print()

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, data):
        self.queue.append(data)
    def dequeue(self):
        if len(self.queue) == 0: return None
        ret = self.queue[0]
        self.queue = self.queue[1:]
        return ret
    def is_empty(self):
        if len(self.queue) == 0: return True
        else:return False
        

class Search():

    def __init__(self, maze, start_pos):
        self.maze = maze
        self.history = copy.deepcopy(maze)
        self.queue = Queue()
        self.queue.enqueue([start_pos])
        
        self.directions = np.array([
                                    [1,0],
                                    [-1,0],
                                    [0,1],
                                    [0,-1]
                                    ])
        self.route = None

    def search(self):
        while not self.queue.is_empty():
            node = self.queue.dequeue()
            pos = node[-1]
            if self.maze[pos[0]][pos[1]] == 3:
                self.route = node
                return node
            self.history[pos[0]][pos[1]] = 4
            maze.print_maze(self.history)
            time.sleep(0.3)

            for dx,dy in self.directions:
                next_pos = [pos[0]+dx,pos[1]+dy]
                if not self._is_wall(next_pos) \
                        and self.history[next_pos[0]][next_pos[1]] != 4:
                    n = node[:]
                    n.append(next_pos)
                    self.queue.enqueue(n)
        return False

    def _is_wall(self, pos):
        if self.maze[pos[0]][pos[1]] == 1:
            return True
        else:return False

if __name__ == "__main__":
    width = 21
    height = 21

    maze = Maze([width, height])
#   maze.create_maze([1,1],[width-2,height-2])
    m = maze.create_maze([1,1])
    maze.print_maze()

    s = Search(m,maze.start_pos)
    s.search()

