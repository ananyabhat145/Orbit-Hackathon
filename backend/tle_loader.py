from sgp4.api import Satrec
from sgp4.conveniences import sat_epoch_datetime
import unicodedata


def load_tles(path: str):
    """
    Reads TLEs in:
    NAME
    LINE1
    LINE2
    """
    sats = []

    # Open file safely with utf-8 and ignore bad characters
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    for i in range(0, len(lines), 3):
        # Clean satellite name to ASCII
        raw_name = lines[i]
        name = unicodedata.normalize('NFKD', raw_name).encode('ascii', 'ignore').decode('ascii')

        l1 = lines[i + 1]
        l2 = lines[i + 2]

        sat = Satrec.twoline2rv(l1, l2)
        sats.append({
            "name": name,
            "satrec": sat,
            "epoch": sat_epoch_datetime(sat)
        })

    return sats
