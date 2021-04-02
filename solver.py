import puzzle
# import custom_structures
import copy
import math
# import metric


class Solver:
    def __init__(self, input_list):
        pass

    def solvable(self, input_list):
        """Determine if a given input grid is solvable.

        It turns out that a lot of grids are unsolvable.
        http://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable/838818
        http://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html

        This implementation assumes blank tile goal position is bottom right.
        """

        # solvability depends on the width...
        width = int(math.sqrt(len(input_list)))

        # ..whether the row that zero is on is odd/even
        # TODO: sort this list/grid confusion
        temp_grid = puzzle.Puzzle(puzzle.list_to_grid(input_list))

        # TODO: see todo on grid.py:65 shouldn't be passing temp_grid.state
        # to a method of temp_grid
        zero_location = temp_grid.locate_tile(0, temp_grid.state)
        if zero_location[0] % 2 == 0:
            y_is_even = True
        else:
            y_is_even = False

        # .. and the number of 'inversions' (not counting '0')

        # strip the blank tile
        input_list = [number for number in input_list if number != 0]

        inversion_count = 0
        list_length = len(input_list)

        for index, value in enumerate(input_list):
            for value_to_compare in input_list[index + 1: list_length]:
                if value > value_to_compare:
                    inversion_count += 1

        if inversion_count % 2 == 0:
            inversions_even = True
        else:
            inversions_even = False

        if width % 2 == 0:
            width_even = True
        else:
            width_even = False

        # our zero_location tuple counts rows from the top,
        # but this algorithm needs to count from the bottom
        if width_even:
            zero_odd = not y_is_even
        # if width not even, we don't need zero_odd (see docstring links)

        # see the bham.ac.uk link
        return ((not width_even and inversions_even)
                or
                (width_even and (zero_odd == inversions_even)))
