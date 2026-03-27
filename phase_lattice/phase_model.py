class PhaseModel:

    def __init__(self, traversal):
        self.path = traversal.path
        self.N = len(self.path)
        self.phase = {}

        for i, s in enumerate(self.path):
            theta = (720.0 / self.N) * i
            self.phase[s] = theta

    def get_phase(self, state):
        return self.phase[state]

    def quadrant(self, theta):
        theta = theta % 720

        if theta < 180:
            return "Q1"
        elif theta < 360:
            return "Q2"
        elif theta < 540:
            return "Q3"
        else:
            return "Q4"