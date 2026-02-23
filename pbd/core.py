from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence, Tuple

Vec3 = List[float]


def v_add(a: Vec3, b: Vec3) -> Vec3:
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def v_sub(a: Vec3, b: Vec3) -> Vec3:
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def v_mul(a: Vec3, s: float) -> Vec3:
    return [a[0] * s, a[1] * s, a[2] * s]


def v_norm(a: Vec3) -> float:
    return sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


@dataclass
class ParticleSystem:
    positions: List[Vec3]
    velocities: List[Vec3]
    inverse_masses: List[float]

    @classmethod
    def from_positions(
        cls,
        positions: Sequence[Sequence[float]],
        masses: Sequence[float],
        initial_velocities: Sequence[Sequence[float]] | None = None,
    ) -> "ParticleSystem":
        if not positions:
            raise ValueError("positions must not be empty")

        pos = [list(map(float, p)) for p in positions]
        if any(len(p) != 3 for p in pos):
            raise ValueError("positions must have shape (n, 3)")

        if len(masses) != len(pos):
            raise ValueError("masses length must match number of particles")
        if any(m < 0.0 for m in masses):
            raise ValueError("mass cannot be negative")

        inv_masses = [0.0 if m == 0.0 else 1.0 / float(m) for m in masses]

        if initial_velocities is None:
            vel = [[0.0, 0.0, 0.0] for _ in pos]
        else:
            vel = [list(map(float, v)) for v in initial_velocities]
            if len(vel) != len(pos) or any(len(v) != 3 for v in vel):
                raise ValueError("initial_velocities must have same shape as positions")

        return cls(pos, vel, inv_masses)


@dataclass
class DistanceConstraint:
    i: int
    j: int
    rest_length: float

    def project(self, predicted: List[Vec3], inv_masses: List[float]) -> None:
        p_i = predicted[self.i]
        p_j = predicted[self.j]
        w_i = inv_masses[self.i]
        w_j = inv_masses[self.j]

        w_sum = w_i + w_j
        if w_sum == 0.0:
            return

        d = v_sub(p_i, p_j)
        dist = v_norm(d)
        if dist < 1e-12:
            return

        c = dist - self.rest_length
        n = v_mul(d, 1.0 / dist)

        correction = c / w_sum

        predicted[self.i] = v_sub(predicted[self.i], v_mul(n, w_i * correction))
        predicted[self.j] = v_add(predicted[self.j], v_mul(n, w_j * correction))


class PBDSimulator:
    def __init__(
        self,
        particles: ParticleSystem,
        constraints: Iterable[DistanceConstraint],
        gravity: Tuple[float, float, float] = (0.0, -9.81, 0.0),
        iterations: int = 10,
    ) -> None:
        self.particles = particles
        self.constraints: List[DistanceConstraint] = list(constraints)
        self.gravity = [float(gravity[0]), float(gravity[1]), float(gravity[2])]
        self.iterations = iterations

    def step(self, dt: float) -> None:
        if dt <= 0:
            raise ValueError("dt must be positive")

        x = self.particles.positions
        v = self.particles.velocities
        w = self.particles.inverse_masses

        for idx, wi in enumerate(w):
            if wi > 0.0:
                v[idx] = v_add(v[idx], v_mul(self.gravity, dt))

        predicted = [v_add(xi, v_mul(vi, dt)) for xi, vi in zip(x, v)]

        for _ in range(self.iterations):
            for c in self.constraints:
                c.project(predicted, w)

        for i in range(len(x)):
            v[i] = v_mul(v_sub(predicted[i], x[i]), 1.0 / dt)
            x[i] = predicted[i]

    def run(self, dt: float, steps: int) -> List[List[Vec3]]:
        trajectory: List[List[Vec3]] = [[p[:] for p in self.particles.positions]]
        for _ in range(steps):
            self.step(dt)
            trajectory.append([p[:] for p in self.particles.positions])
        return trajectory
