import sys
import solver
from math import sqrt


def print_usage():
    print("python main.py <puzzle>")
    print("e.g: python main.py 0,1,2,3,4,5,6,7,8")
    print("Where 0 is blank cell")


def is_square_number(number):
    if not sqrt(number).is_integer():
        return False
    return True


def main(argv):
    if len(argv) < 1:
        print_usage()
        sys.exit()

    # convert input string to a list of integers
    input_list = argv[0].split(',')
    input_list = list(map(int, input_list))

    if not is_square_number(len(input_list)):
        raise Exception(
            "Error: input grid must be nxn square")

    ordered_list = sorted(input_list)
    for index, number in enumerate(ordered_list):
        if number != index:
            raise Exception(
                "Error: input list must contain all numbers from 0 to n^2 - 1")


if __name__ == "__main__":
    main(sys.argv[1:])
