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

    def __init__(self, input_state):

        # don't just bind to input state. we want the object to have its OWN state
        # https://docs.python.org/2/library/copy.html
        self.state = copy.deepcopy(input_state)

        self.path_history = list()

        # TODO: we're calculating n here, but passing it between objects elsewhere. Tidy?
        self.n = len(input_state[0])

    def locate_tile(self, tile, puzzle_state):
        """Return the co-ordinates of a given tile, given as a tuple.
        Assumes one unique tile in grid."""

        # TODO: should this be a static method: doesn't always operate on self?
        for (y, row) in enumerate(puzzle_state):
            for (x, value) in enumerate(row):
                if value == tile:
                    return (y, x)
