from sgp4.api import Satrec
from sgp4.conveniences import sat_epoch_datetime

def load_tles(path: str):
    sats = []
    with open(path, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    for i in range(0, len(lines), 3):
        name = lines[i]
        l1 = lines[i + 1]
        l2 = lines[i + 2]
        sat = Satrec.twoline2rv(l1, l2)
        sats.append({
            "name": name,
            "satrec": sat,
            "epoch": sat_epoch_datetime(sat)
        })

    return sats
