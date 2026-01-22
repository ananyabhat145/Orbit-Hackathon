import numpy as np

def propagate_satellite(position, velocity, minutes_ahead):
    dt = 60  # seconds
    steps = minutes_ahead

    r = np.array(position, dtype=float)
    v = np.array(velocity, dtype=float)

    traj = []

    for _ in range(steps):
        r = r + v * dt
        traj.append(r.tolist())

    return traj
