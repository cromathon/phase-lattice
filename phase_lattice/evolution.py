class Evolution:

    def __init__(self, ida, traversal, phase, orbit):

        self.ida = ida
        self.traversal = traversal
        self.phase = phase
        self.orbit = orbit

    def step_traversal(self, state):

        return self.traversal.next_state(state)

    def step_inversion(self, state):

        return self.orbit.invert(state)

    def neighbors(self, state):

        return self.ida.neighbors(state)
