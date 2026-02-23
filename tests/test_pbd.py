from math import sqrt

from pbd import DistanceConstraint, PBDSimulator, ParticleSystem


def _dist(a, b):
    d0 = a[0] - b[0]
    d1 = a[1] - b[1]
    d2 = a[2] - b[2]
    return sqrt(d0 * d0 + d1 * d1 + d2 * d2)


def test_distance_constraint_is_preserved_after_step():
    rest = 1.0
    particles = ParticleSystem.from_positions(
        positions=[[0.0, 0.0, 0.0], [1.2, 0.0, 0.0]],
        masses=[0.0, 1.0],
    )
    sim = PBDSimulator(
        particles,
        constraints=[DistanceConstraint(0, 1, rest_length=rest)],
        gravity=(0.0, 0.0, 0.0),
        iterations=20,
    )

    sim.step(1 / 60)

    dist = _dist(sim.particles.positions[0], sim.particles.positions[1])
    assert abs(dist - rest) < 1e-6


def test_fixed_particle_does_not_move_under_gravity():
    particles = ParticleSystem.from_positions(
        positions=[[0.0, 1.0, 0.0], [0.0, 0.0, 0.0]],
        masses=[0.0, 1.0],
    )
    sim = PBDSimulator(
        particles,
        constraints=[DistanceConstraint(0, 1, rest_length=1.0)],
        iterations=10,
    )

    x0 = [p[:] for p in sim.particles.positions]
    sim.step(1 / 60)

    assert sim.particles.positions[0] == x0[0]


def test_free_particles_split_correction_equally():
    particles = ParticleSystem.from_positions(
        positions=[[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
        masses=[1.0, 1.0],
    )
    sim = PBDSimulator(
        particles,
        constraints=[DistanceConstraint(0, 1, rest_length=1.0)],
        gravity=(0.0, 0.0, 0.0),
        iterations=1,
    )

    sim.step(1 / 60)

    assert sim.particles.positions[0][0] == 0.5
    assert sim.particles.positions[1][0] == 1.5
