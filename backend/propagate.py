import numpy as np
from datetime import timedelta


def propagate_satellite(satrec, start_time, minutes_ahead=1440, step=10):
    """
    Returns positions over time in km.
    """
    positions = []

    for t in range(0, minutes_ahead, step):
        future_time = start_time + timedelta(minutes=t)
        jd, fr = satrec.jdsatepoch, satrec.jdsatepochF + (t / 1440.0)

        e, r, v = satrec.sgp4(jd, fr)

        if e == 0:
            positions.append({
                "t": t,
                "pos": np.array(r)
            })

    return positions

