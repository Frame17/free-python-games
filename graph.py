import collections
from collections import defaultdict
import random
import queue as Q


def is_acceptable(current, next):
    """
    check if the next tile is acceptable from the current in 1 step
    :param current: current tile
    :param next: next tile
    :return: boolean
    """
    return abs(current - next) == 20 or abs(current - next) == 1


def add_back_road(path, tile):
    """
    return to the tile that is acceptable from the tile
    :param path: list of indexes
    :param tile: next tile index
    """
    i = len(path) - 1
    while not is_acceptable(path[i], tile):
        path.append(path[i - 1])
        i -= 1


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
        self.tiles = tiles
        self.offset = offset

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
                    if not is_acceptable(path[len(path) - 1], neighbour):
                        add_back_road(path, neighbour)
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
        path = []
        q = [start]
        while q:
            v = q.pop(0)
            if v not in path:
                if len(path) > 1 and not is_acceptable(path[len(path) - 1], v):
                    add_back_road(path, v)
                path.append(v)
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
        visited = set()

        while not queue.empty():
            node = queue.get()
            current = node[1][len(node[1]) - 1]

            if target in node[1]:
                return node[1]

            cost = node[0]
            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    temp = node[1][:]
                    temp.append(neighbor)
                    queue.put((cost + default_cost, temp))

        return None

    def Greedy(self, start, end):
        """
        Greedy algorithm implementation
        :param start: starting point
        :param end: point with a prize
        :return: list of path indexes that were lead from root to the target
        """
        path = []
        visited = [end]
        curr = end
        prev = end
        while curr != start:
            next_opts = list(filter(lambda v: v not in visited, adj(curr)))
            if not next_opts:
                next_opts = list(filter(lambda v: v != prev, adj(curr)))
            closest = random.choice(next_opts)
            path.append(closest)
            visited.append(closest)
            prev = curr
            curr = closest

        path.reverse()
        return path

    def AStar(self, start, end):
        """
        A* implementation
        :param start: starting point
        :param end: point with a prize
        :return: list of path indexes that were lead from root to the target
        """

        class Node():
            """A node class for A* Pathfinding"""

            def __init__(self, parent=None, position=None):
                self.parent = parent
                self.position = position

                self.g = 0
                self.h = 0
                self.f = 0

            def __eq__(self, other):
                return self.position == other.position

        # Create start and end node
        # start = get_2d_index(self.tiles, start)
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        # end = get_2d_index(self.tiles, end)
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list

        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

                # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in [-1, 1, -self.offset, self.offset]:#, (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

                # Get node position
                node_position = current_node.position + new_position

                # Make sure within range
                if node_position > (len(self.tiles) - 1) or node_position < 0:
                    continue

                # Make sure walkable terrain
                if self.tiles[node_position] == 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                if new_node in closed_list:
                    continue

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = (child.position - end_node.position) ** 2
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)


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


def adj(v):
    adj = []
    if tiles[v + 1] == 1:
        adj.append(v + 1)
    if tiles[v - 1] == 1:
        adj.append(v - 1)
    if tiles[v + 20] == 1:
        adj.append(v + 20)
    if tiles[v - 20] == 1:
        adj.append(v - 20)
    return adj


def print_path(path):
    """
    print path to the target
    :param path: list of roads
    """
    print(" -> ".join(map(str, path)))


if __name__ == '__main__':

    roads = get_roads(tiles)

    g = Graph(tiles)

    # 52, 161 for testing perpose
    starting_point = random.choice(roads)
    prize = random.choice(roads)
    #
    # path = g.BFS(starting_point, prize)
    # print(f"BFS path({len(path)} steps) from starting point {starting_point} to target point {prize}:")
    # print_path(path)

    # print("----")

    # path = g.DFS(starting_point, prize)
    # print(f"DFS path({len(path)} steps) from starting point {starting_point} to target point {prize}:")
    # print_path(path)

    # print("----")

    path = g.UCS(starting_point, prize)
    print(
        f"UCS path({len(path)} steps, cost = {len(path) - 1}) from starting point {starting_point} to target point {prize}:")
    print_path(path)

    print("----")

    path = g.Greedy(starting_point, prize)

    print(
        f"Greedy path({len(path)} steps) from starting point {starting_point} to target point {prize}:")
    print_path(path)

    print("----")

    path = g.AStar(starting_point, prize)

    print(
        f"A* path({len(path)} steps) from starting point {starting_point} to target point {prize}:")
    print_path(path)
