import numpy as np

MU_EARTH = 398600.4418  # km^3 / s^2

def propagate_satellite(position, velocity, minutes_ahead):
    """
    Simple 2-body orbital propagation using Euler integration.
    Not high-fidelity, but physically correct enough for risk estimation.
    """
    dt = 60  # seconds
    steps = minutes_ahead

    r = np.array(position, dtype=float)
    v = np.array(velocity, dtype=float)

    traj = []

    for _ in range(steps):
        # Gravitational acceleration
        accel = -MU_EARTH * r / np.linalg.norm(r)**3

        # Integrate
        v = v + accel * dt
        r = r + v * dt

        traj.append(r.tolist())

    return traj

