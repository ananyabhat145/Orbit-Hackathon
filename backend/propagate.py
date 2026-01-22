def propagate_satellite(position, velocity, minutes_ahead):
    """
    Simple two-body propagation.
    position: [x, y, z] km
    velocity: [vx, vy, vz] km/s
    """
    dt = 60  # seconds
    steps = minutes_ahead

    traj = []
    r = np.array(position, dtype=float)
    v = np.array(velocity, dtype=float)

    for i in range(steps):
        r = r + v * dt
        traj.append(r.tolist())

    return traj
