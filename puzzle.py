import copy
import math


def list_to_grid(input_list):
    """Take a list of length n^2, return a nxn 2D list"""

    n = int(math.sqrt(len(input_list)))

    # initialise empty grid
    grid = [['-' for x in range(n)] for y in range(n)]

    # populate grid with tiles
    i = 0
    j = 0
    for tile in input_list:
        grid[i][j] = tile
        j += 1
        if j == n:
            j = 0
            i += 1

    return grid


class Puzzle:
    """Represent the state of a puzzle: state, path_history"""

    def __init__(self, state, ancestors=[], previous_move="None", depth=0):

        # don't just bind to input state. we want the object to have its OWN state
        # https://docs.python.org/2/library/copy.html
        self.state = copy.deepcopy(state)
        self.ancestors = copy.copy(ancestors)
        self.previous_move = previous_move
        self.depth = depth

        # TODO: we're calculating n here, but passing it between objects elsewhere. Tidy?
        self.n = len(state[0])

    def __str__(self):
        display = f'Step: {self.depth}'
        for row in self.state:
            display += f'\n{row}'
        return display

    def move(self, direction):
        """Slide a tile in one of 4 directions.

        Return True if successful (with side-effect of changing the state input).
        Return False if movement in that direction not possible. 
        """

        # if new direction will return parent state, then stop moving, return None
        if (direction == "up" and self.previous_move == "down"):
            return None
        elif (direction == "down" and self.previous_move == "up"):
            return None
        elif (direction == "left" and self.previous_move == "right"):
            return None
        elif (direction == "right" and self.previous_move == "left"):
            return None

        (old_y, old_x) = self.locate_tile(0, self.state)

        # find the offset of the moving tile relative to the '0' tile
        # when we say 'move left' we mean the tile, not the space (0)
        delta_x, delta_y = 0, 0
        if direction == 'up':
            delta_y = 1
        elif direction == 'down':
            delta_y = -1
        elif direction == 'left':
            delta_x = -1
        elif direction == 'right':
            delta_x = 1
        else:
            raise Exception(
                "Invalid move! Must be 'up', 'down', or 'left', 'right'")

        new_x = old_x + delta_x
        new_y = old_y + delta_y
        # return false if move not possible
        valid_range = range(0, self.n)
        if new_y not in valid_range or new_x not in valid_range:
            return False

        # swap tiles, update node properties, return new Node
        new_state = copy.deepcopy(self.state)
        new_state[old_x][old_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[old_x][old_y]
        self.previous_move = direction
        self.depth += 1

        return True

    def locate_tile(self, tile, puzzle_state):
        """Return the co-ordinates of a given tile, given as a tuple.
        Assumes one unique tile in grid."""
        for (y, row) in enumerate(puzzle_state):
            for (x, value) in enumerate(row):
                if value == tile:
                    return (y, x)

    def copy(self):
        new_node = Puzzle(self.state, self.ancestors,
                          self.previous_move, self.depth)
        return new_node
