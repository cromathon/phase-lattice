class OrbitOps:

    def __init__(self, traversal):
        self.path = traversal.path
        self.N = len(self.path)
        self.half = self.N // 2
        self.index = {s: i for i, s in enumerate(self.path)}

    def invert(self, state):
        i = self.index[state]
        j = (i + self.half) % self.N
        return self.path[j]