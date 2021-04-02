import puzzle
import copy
import math
import random
from collections import deque

# all state from now on are instance of class Puzzle (which is in grid, 2d list)


def does_state_exist(item, list_to_search):
    """Search only `state` properties of members"""
    for element in list_to_search:
        if item.state == element.state:
            return True
    return False


class Solver:
    def __init__(self, input_list):
        """Initialise Solver object. Raise ValueError if solution not possible."""

        if not self.solvable(input_list):
            raise Exception('The puzzle is not solvable')

        self.init_state = copy.deepcopy(puzzle.list_to_grid(input_list))
        self.goal_state = self.set_goal_state(input_list)
        self.depth = 0

        self.stack = deque()
        self.visited = deque()

    def depth_first_search(self):
        """ While stack is not empty,
            pop and expand top of stack until goal found"""
        init_puzzle = puzzle.Puzzle(self.init_state)
        self.stack.append(init_puzzle)

        while self.stack:
            node = self.stack.pop()
            print(f'Stack len: {len(self.stack)}')

            self.visited.append(node)
            self.depth += 1

            if node.state == self.goal_state:
                print("GOAL FOUND")
                return node.ancestors

            self.expand_nodes(node)

        # The method should not go here
        raise Exception("Something went wrong in DFS, this line should not be reached")

    def expand_nodes(self, node):
        moves_list = ["up", "down", "left", "right"]
        # random.shuffle(moves_list)

        for direction in moves_list:
            new_node = node.copy()

            if new_node.move(direction):
                new_node.ancestors.append(node)

            if does_state_exist(new_node, self.stack) and does_state_exist(new_node, self.visited):
                self.stack.append(new_node)

    def set_goal_state(self, input_list):
        ordered_list = sorted(input_list)
        # Bring blank cell from first index to the end
        ordered_list.pop(0)
        ordered_list.append(0)

        goal_state = puzzle.list_to_grid(ordered_list)
        return goal_state

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
