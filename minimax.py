import graph
import math

class Minimax:

    # Constructor
    def __init__(self, tiles):
        self.tiles = tiles
        self.g = graph.Graph(tiles)

    def is_moves_left(self, tiles):
        """
        Check if there are moves left in the maze
        TODO: add current position if the agent is Pacman and check if the move that was made leads to the ghost
        :param tiles: maze
        :return: True if there are coins left in the maze
        """
        return len([tile for tile in tiles if tile == 1]) > 0

    def evaluate(self, tiles, pacman, ghost):
        """
        Evaluation function
        Evaluate the move was made for each agent
        :param tiles: maze
        :param pacman: pacman position
        :param ghost: ghost position
        :return: +10 if Pacman has won in this move, -10 if ghost has eaten the pacman(pacman lost), 0 otherwise
        """

        # pacman has eaten all coins
        if not len([tile for tile in tiles if tile == 1]):
            return 10

        # ghost has eaten the pacman
        if ghost == pacman:
            return -10

        # nobody won
        return 0

    def closest_coin(self, tiles, pacman):
        """
        Get the closest coin to the pacman position
        :param tiles: maze
        :param pacman: pacman position
        :return: coin index
        """
        coin = math.inf
        min_distance = math.inf

        def convert_from_raw(raw_pos):
            # complex high-level mathematics
            x = (raw_pos % 20) * 20 - 200
            y = 180 - (raw_pos // 20) * 20
            return x, y

        pac_x, pac_y = convert_from_raw(pacman)
        pacman_vec = (pac_x, pac_y)

        for i, tile in enumerate(tiles):
            if tile == 1:
                coin_x, coin_y = convert_from_raw(i)
                coin_vec = (coin_x, coin_y)
                distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(coin_vec, pacman_vec)]))
                if distance < min_distance:
                    coin = i
                    min_distance = distance

        return coin

    def minimax(self, tiles, pacman, ghost, depth, is_max):
        """
        Minimax algorithm
        It considers all the possible ways the game can go
        :param tiles: maze
        :param pacman: pacman position
        :param ghost: ghost position
        :param depth: depth of the current move
        :param is_max: is agent Maximizer or Minimizer
        :return: the value of moves
        """

        score = self.evaluate(tiles, pacman, ghost)

        # Maximizer or Minimizer won the game
        if score == -10 or score == 10:
            return score

        # limit moves by depth
        if depth >= 100:
            return score

        # pacman's move
        if is_max:
            best = -math.inf

            coin = self.closest_coin(tiles, pacman)
            path = self.g.UCS(pacman, coin)
            move = path[0]

            # eat the coin
            if tiles[move] == 1:
                tiles[move] = 2
            # make the move
            pacman = move
            # call minimax
            best = max(best, self.minimax(tiles, pacman, ghost, depth + 1, not is_max))

            # undo the move
            if tiles[move] == 2:
                tiles[move] = 1

            return best

        # ghost's move
        else:
            best = math.inf

            path = self.g.UCS(ghost, pacman)
            move = path[0]
            ghost = move
            best = min(best, self.minimax(tiles, pacman, ghost, depth + 1, not is_max))

            return best

    def find_best_move(self, tiles, pacman, ghosts, is_pacman):
        """
        Find best move for the agent
        :param tiles: maze
        :param pacman: pacman position
        :param ghosts: list of ghosts positions
        :param is_pacman: finding best move as for pacman or not
        :return: best move for the player
        """

        if is_pacman:
            best_val = -math.inf
            best_move = -math.inf

            for ghost in ghosts:
                coin = self.closest_coin(tiles, pacman)
                path = self.g.UCS(pacman, coin)
                move = path[0]

                # eat the coin
                if tiles[move] == 1:
                    tiles[move] = 2
                # make the move
                pacman = move
                move_val = self.minimax(tiles, pacman, ghost, 0, False)

                # undo the move
                if tiles[move] == 2:
                    tiles[move] = 1

                if move_val > best_val:
                    best_val = move_val
                    best_move = move

            return best_move

        else:

            return [self.g.UCS(ghost, pacman)[0] for ghost in ghosts]



if __name__ == '__main__':
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

    pacman = 103
    ghosts = [22]

    minimax = Minimax(tiles)
    pacman_move = minimax.find_best_move(tiles, pacman, ghosts, True)
    print(pacman_move)
