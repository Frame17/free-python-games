from turtle import *
from freegames import floor, vector
import random
import time
from graph import Graph
from minimax import Minimax
import tracemalloc

state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = None
pacman_raw = None
# ghosts = [
#     [vector(-180, 160), vector(20, 0)],
#     [vector(-180, -160), vector(0, 20)],
#     [vector(100, 160), vector(0, -20)],
#     [vector(100, -160), vector(-20, 0)]
# ]
num_ghosts = 1 #for now
ghosts = []
ghosts_raw = []
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


def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    global pacman
    global pacman_raw
    "Draw world using path."
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

    pac_x, pac_y, pac_raw = random_init()
    pacman = vector(pac_x, pac_y)
    pacman_raw = pac_raw

    can_x, can_y, can_raw = random_init()
    while can_x == pac_x and can_y == pac_y:  # reinit in case of collision
        can_x, can_y, _ = random_init()
    path.up()
    path.goto(can_x + 10, can_y + 10)
    path.dot(5, 'white')

    # init ghosts
    for i in range(num_ghosts):
        ghost_x, ghost_y, ghost_raw = random_init()
        while ghost_x == pac_x and ghost_y == pac_y:  # reinit in case of collision
            ghost_x, ghost_y, ghost_raw = random_init()
        ghost = vector(ghost_x, ghost_y)
        ghosts.append(ghost)
        ghosts_raw.append(ghost_raw)


def move(point, way, is_pacman):
    """Move point"""
    writer.undo()
    writer.write(state['score'])

    clear()

    point.move(way)

    if is_pacman:
        index = offset(point)

        if tiles[index] == 1:
            tiles[index] = 2
            state['score'] += 1
            x, y = convert_from_raw(index)
            square(x, y)

    up()
    goto(point.x + 10, point.y + 10)

    if is_pacman:
        dot(20, 'yellow')
    else:
        dot(20, 'red')

    update()


def convert_from_raw(raw_pos):
    # complex high-level mathematics
    x = (raw_pos % 20) * 20 - 200
    y = 180 - (raw_pos // 20) * 20
    return x, y


def random_init():
    raw_pos = random.randint(0, len(tiles))
    if tiles[raw_pos] == 0:
        while tiles[raw_pos] != 1:
            raw_pos = (raw_pos + 1) % len(tiles)

    x, y = convert_from_raw(raw_pos)

    return x, y, raw_pos


def is_end():
    # ghost has eaten the pacman or pacman has eaten all coins
    return len([ghost for ghost in ghosts if ghost == pacman]) or not len([tile for tile in tiles if tile == 1])


def agent_move(prev, next, is_pacman):
    x, y = convert_from_raw(prev)
    point = vector(x, y)
    if next == prev + 1:
        move(point, vector(20, 0), is_pacman)
    elif next == prev - 1:
        move(point, vector(-20, 0), is_pacman)
    elif next < prev:
        move(point, vector(0, 20), is_pacman)
    elif next > prev:
        move(point, vector(0, -20), is_pacman)


def play():
    global pacman_raw
    minimax = Minimax(tiles)
    while not is_end():
        tiles[pacman_raw] = 2
        pacman_move = minimax.find_best_move(tiles, pacman_raw, ghosts_raw, True)
        agent_move(pacman_raw, pacman_move, True)
        pacman_raw = pacman_move

        for i, ghost_move in enumerate(minimax.find_best_move(tiles, pacman_raw, ghosts_raw, False)):
            agent_move(ghosts_raw[i], ghost_move, False)
        time.sleep(0.3)


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
world()
play()