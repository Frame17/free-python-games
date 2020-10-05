import collections
from collections import defaultdict
import random
import queue as Q


# This class represents a directed graph
# using adjacency list representation
class Graph:

    # Constructor
    def __init__(self, tiles, offset=20):
        """
        create a graph from the 1d array
        :param tiles: 1d array with tiles
        :param offset: row offset
        """
        # default dictionary to store graph
        self.graph = defaultdict(list)

        for (i, tile) in enumerate(tiles):
            # if tile is a wall
            if tile != 1:
                continue

            # left
            if i != 0:
                left = i - 1
                left_tile = tiles[left]
                if left_tile != 0:
                    self.add_edge(i, left)
            # right
            if i != len(tiles) - 1:
                right = i + 1
                right_tile = tiles[right]
                if right_tile != 0:
                    self.add_edge(i, right)
            # top
            if i > offset:
                top = i - offset
                top_tile = tiles[top]
                if top_tile != 0:
                    self.add_edge(i, top)

            # bottom
            if i > offset:
                bottom = i + offset
                bottom_tile = tiles[bottom]
                if bottom_tile != 0:
                    self.add_edge(i, bottom)

    def add_edge(self, u, v):
        """
        Add and edge to graph
        :param u: from
        :param v: to
        """
        self.graph[u].append(v)

    def BFS(self, start, target):
        """
        BFS implementation
        :param start: starting point
        :param target: point with a prize
        :return: list of path indexes that were lead from root to the target
        """
        visited, queue, path = set(), collections.deque([start]), [start]

        visited.add(start)
        while queue:
            vertex = queue.popleft()
            for neighbour in self.graph[vertex]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
                    path.append(neighbour)
                    # target reached
                    if neighbour == target:
                        return path

        return None

    def DFS(self, start, target):
        """
        DFS implementation
        :param start: starting point
        :param target: point with a prize
        :return: list of path indexes that were lead from root to the target
        """
        # if visited is None:
        #     visited = set()
        #     self.path = []
        #
        # if start != target:
        #     self.path.append(start)
        #
        # visited.add(start)
        #
        # for next_index in set(self.graph[start]) - visited:
        #     self.DFS(next_index, target, visited)
        path = []
        q = [start]
        while q:
            v = q.pop(0)
            if v not in path:
                path = path + [v]
                if v == target:
                    return path
                q = self.graph[v] + q
        return None

    def UCS(self, start, target):
        """
        UCS implementation
        :param start: starting point
        :param target: point with a prize
        :return: list of path indexes that were lead from root to the target and cost
        """
        # cost for each step is 1 as discussed on the practice lesson
        default_cost = 1
        queue = Q.PriorityQueue()
        queue.put((0, [start]))

        while not queue.empty():
            node = queue.get()
            current = node[1][len(node[1]) - 1]

            if target in node[1]:
                return node[1], node[0]

            cost = node[0]
            for neighbor in self.graph[current]:
                temp = node[1][:]
                temp.append(neighbor)
                queue.put((cost + default_cost, temp))

        return None, 0

tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]


# 0 is a wall

def get_roads(tiles):
    """
    get only roads
    :param tiles: list of tiles
    :return: list of index with roads only
    """
    return [i for (i, tile) in enumerate(tiles) if tile == 1]


def print_path(path):
    """
    print path to the target
    :param path: list of roads
    """
    print(" -> ".join(map(str, path)))


if __name__ == '__main__':

    g = Graph(tiles)

    roads = get_roads(tiles)

    starting_point = random.choice(roads)
    prize = random.choice(roads)

    path = g.BFS(starting_point, prize)
    print(f"BFS path({len(path)} steps) from starting point {starting_point} to target point {prize}:")
    print_path(path)

    print("----")

    path = g.DFS(starting_point, prize)
    print(f"DFS path({len(path)} steps) from starting point {starting_point} to target point {prize}:")
    print_path(path)

    print("----")

    path, cost = g.UCS(starting_point, prize)
    print(f"UCS path({len(path)} steps, cost = {cost}) from starting point {starting_point} to target point {prize}:")
    print_path(path)