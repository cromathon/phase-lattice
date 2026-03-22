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


def complex_sum(signal):
    total = 0j
    for amp, phase in signal.values():
        total += amp * cmath.exp(1j * math.radians(phase))
    return total


def run_demo():
    engine = build_system(3)

    print("\n=== Destructive Interference Demo ===")

    # two signals, same node, opposite phase
    a = 1.0 * cmath.exp(1j * math.radians(0.0))
    b = 1.0 * cmath.exp(1j * math.radians(180.0))

    total = a + b

    print("\nTwo signals at same state:")
    print("  amplitude=1.0 @ 0°")
    print("  amplitude=1.0 @ 180°")

    print("\nCombined (complex):")
    print(f"  magnitude = {abs(total):.6f}")
    print(f"  phase = {math.degrees(cmath.phase(total)):.2f}")

    print("\nResult:")
    print("  → perfect cancellation (amplitude ≈ 0)")

    print("\nNow propagate through system:")

    signal = {
        (0, 0, 0): (0.0, 0.0)  # cancellation already happened
    }

    signal = engine.step(signal)

    print("\nAfter one step:")
    print(signal)

    print("\n--- Notice ---")
    print("• signal vanished before propagation")
    print("• interference determines existence")


if __name__ == "__main__":
    run_demo()
