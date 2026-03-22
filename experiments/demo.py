
from phase_lattice.ida import IDA
from phase_lattice.traversal import Traversal
from phase_lattice.phase_model import PhaseModel
from phase_lattice.orbit_ops import OrbitOps
from phase_lattice.evolution import Evolution
from phase_lattice.operators import Operators
from phase_lattice.signal_engine import SignalEngine
from phase_lattice.phase_engine import PhaseEngine


import math
import cmath


# ----------------------------
# Build system
# ----------------------------
def build_system(n=3):
    ida = IDA(n)
    traversal = Traversal(n)
    phase = PhaseModel(traversal)
    orbit = OrbitOps(traversal)
    evo = Evolution(ida, traversal, phase, orbit)
    ops = Operators(evo)
    phase_engine = PhaseEngine(phase)
    engine = SignalEngine(ida, traversal, orbit, phase_engine)
    return engine


# ----------------------------
# Helpers
# ----------------------------
def complex_sum(signal):
    total = 0j
    for amp, phase in signal.values():
        total += amp * cmath.exp(1j * math.radians(phase))
    return total


def normalize(signal):
    total = sum(abs(amp) for amp, _ in signal.values())
    if total == 0:
        return signal
    return {s: (amp / total, ph) for s, (amp, ph) in signal.items()}


def top_states(signal, k=4):
    return sorted(signal.items(), key=lambda x: -x[1][0])[:k]


# ----------------------------
# Demo
# ----------------------------
def run_demo():
    engine = build_system(3)

    print("\n=== Phase-Coherent Signal Demo ===")

    signal = {
        (0, 0, 0): (1.0, 0.0),
        (1, 1, 1): (1.0, 0.0),
    }

    print("\nInitial signal:")
    print(signal)

    for step in range(1, 9):
        signal = engine.step(signal)
        signal = normalize(signal)

        vec = complex_sum(signal)

        print(f"\nStep {step}")
        print(f"  total_amp = {sum(a for a, _ in signal.values()):.4f}")
        print(f"  vector_mag = {abs(vec):.4f}")
        print(f"  vector_phase = {math.degrees(cmath.phase(vec)):.2f}")

        print("  top states:")
        for s, (amp, ph) in top_states(signal):
            print(f"    {s} → amp={amp:.4f}, phase={ph:.1f}")

    print("\n--- Result ---")
    print("Notice:")
    print("• signal does NOT spread uniformly")
    print("• certain states dominate")
    print("• system stabilizes via interference")


if __name__ == "__main__":
    run_demo()
