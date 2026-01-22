import math
import numpy as np

MU_EARTH = 398600.4418  # km^3 / s^2
R_EARTH = 6371  # km


def orbital_elements_to_state_vector(
    perigee_km,
    apogee_km,
    inclination_deg
):
    """
    Convert simplified orbital elements into a state vector.
    Assumes:
    - Argument of perigee = 0
    - RAAN = 0
    - True anomaly = 0 (at perigee)
    """

    # Semi-major axis
    rp = R_EARTH + perigee_km
    ra = R_EARTH + apogee_km
    a = (rp + ra) / 2

    # Velocity at perigee (vis-viva)
    v = math.sqrt(MU_EARTH * (2 / rp - 1 / a))

    inc = math.radians(inclination_deg)

    # Position at perigee
    position = np.array([
        rp,
        0,
        0
    ])

    # Velocity perpendicular to position
    velocity = np.array([
        0,
        v * math.cos(inc),
        v * math.sin(inc)
    ])

    return position.tolist(), velocity.tolist()
