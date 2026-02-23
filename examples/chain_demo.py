"""Run a small PBD chain simulation."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pbd import DistanceConstraint, PBDSimulator, ParticleSystem


def build_chain(n: int = 8, spacing: float = 0.3) -> PBDSimulator:
    positions = [[i * spacing, 0.0, 0.0] for i in range(n)]
    masses = [0.0] + [1.0] * (n - 1)  # first particle fixed
    particles = ParticleSystem.from_positions(positions, masses)

    constraints = [DistanceConstraint(i, i + 1, spacing) for i in range(n - 1)]
    return PBDSimulator(particles, constraints, iterations=15)


def main() -> None:
    sim = build_chain()
    traj = sim.run(dt=1 / 60.0, steps=180)

    print("final positions:")
    for p in traj[-1]:
        print([round(v, 4) for v in p])


if __name__ == "__main__":
    main()
