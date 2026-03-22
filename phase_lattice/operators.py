class Operators:

    def __init__(self, evolution):

        self.evo = evolution

    def apply(self, state, op):

        if op == "T":
            return self.evo.step_traversal(state)

        if op == "I":
            return self.evo.step_inversion(state)

        raise ValueError("Unknown operator")

    def run_sequence(self, start, seq):

        state = start
        path = [state]

        for op in seq:

            state = self.apply(state, op)
            path.append(state)

        return path
