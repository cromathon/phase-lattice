import math


class PhaseEngine:

    def __init__(self, phase_model):
        self.phase = phase_model

    def weight(self, state):
        theta = self.phase.get_phase(state)
        r = math.radians(theta)
        return math.sin(r) + 1.1