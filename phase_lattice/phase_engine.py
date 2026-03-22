import math


class PhaseEngine:

    def __init__(self, phase_model):
        self.phase = phase_model


    def weight(self, state):

        theta = self.phase.get_phase(state)

        # convert to radians
        r = math.radians(theta)

        # simple harmonic weight
        return math.sin(r) + 1.1
