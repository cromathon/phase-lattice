def gray_code(n):
    """
    Generate traversal of R_n where
    successive states differ by one bit
    """

    if n == 0:
        return [()]

    prev = gray_code(n - 1)

    return (
        [(0,) + p for p in prev] +
        [(1,) + p for p in reversed(prev)]
    )


class Traversal:

    def __init__(self, n):
        self.n = n
        self.path = gray_code(n)

    def next_state(self, current):

        i = self.path.index(current)
        return self.path[(i + 1) % len(self.path)]
