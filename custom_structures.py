from collections import deque


class Visited:
    """A stack - LIFO"""

    def __init__(self):
        self.stack = deque()

    def __contains__(self, item):
        """Custom method. Search only `state` properties of elements"""

        for element in self.stack:
            if item.state == element.state:
                return True

        return False
