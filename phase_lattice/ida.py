from itertools import product


class IDA:
    def __init__(self, n):
        self.n = n
        self.states = list(product([0, 1], repeat=n))

    def flip(self, state, axis):
        s = list(state)
        s[axis] ^= 1
        return tuple(s)

    def neighbors(self, state):
        return [self.flip(state, i) for i in range(self.n)]

    def shell(self, state):
        return sum(state)