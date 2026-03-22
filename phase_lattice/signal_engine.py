import math


class SignalEngine:

    def __init__(self, ida, traversal, orbit, phase_engine):
        self.ida = ida
        self.traversal = traversal
        self.orbit = orbit
        self.phase_engine = phase_engine

    # ----------------------------
    # MAIN STEP (SIMULTANEOUS)
    # ----------------------------
    def step(self, signal):
        """
        signal: {state: (amplitude, phase_deg)}
        """

        new_signal = {}

        for state, (amp, phase) in signal.items():

            # --- 1. Neighbor spread ---
            neighbors = self.ida.neighbors(state)

            for n in neighbors:
                w = self.phase_engine.weight(n)
                incoming_amp = amp * w / len(neighbors)

                # phase aligns to target node phase
                target_phase = self.phase_engine.phase.get_phase(n)

                self._accumulate(new_signal, n, incoming_amp, target_phase)

            # --- 2. Traversal ---
            nxt = self.traversal.next_state(state)

            traversal_phase = phase + self._delta_phase()

            self._accumulate(new_signal, nxt, amp, traversal_phase)

            # --- 3. Inversion (half orbit = +360°) ---
            inv = self.orbit.invert(state)

            inversion_phase = phase + 360.0

            self._accumulate(new_signal, inv, amp, inversion_phase)

        return new_signal

    # ----------------------------
    # INTERNALS
    # ----------------------------
    def _delta_phase(self):
        """
        phase step per traversal move
        """
        N = len(self.traversal.path)
        return 720.0 / N

    def _accumulate(self, signal, state, amp, phase):
        """
        combine signals using continuous phase interference
        """

        phase_rad = math.radians(phase)

        # convert to complex representation
        incoming = complex(
            amp * math.cos(phase_rad),
            amp * math.sin(phase_rad)
        )

        if state in signal:
            existing_amp, existing_phase = signal[state]

            existing_rad = math.radians(existing_phase)

            existing = complex(
                existing_amp * math.cos(existing_rad),
                existing_amp * math.sin(existing_rad)
            )

            total = existing + incoming
        else:
            total = incoming

        # convert back to (amp, phase)
        new_amp = abs(total)
        new_phase = math.degrees(math.atan2(total.imag, total.real))

        signal[state] = (new_amp, new_phase)

    # ----------------------------
    # OPTIONAL: NORMALIZATION
    # ----------------------------
    def normalize(self, signal):
        total = sum(abs(amp) for amp, _ in signal.values())

        if total == 0:
            return signal

        return {
            s: (amp / total, phase)
            for s, (amp, phase) in signal.items()
        }