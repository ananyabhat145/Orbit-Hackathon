import numpy as np

# Distance (km) under which we consider a potential collision
COLLISION_DISTANCE_KM = 1.0


def collision_probability(traj_a, traj_b, samples=300):
    """
    Monte Carlo estimate of collision probability between two trajectories.
    traj_a / traj_b: lists of (x, y, z) positions in km
    """
    if not traj_a or not traj_b:
        return 0.0

    min_len = min(len(traj_a), len(traj_b))
    hits = 0

    for _ in range(samples):
        idx = np.random.randint(0, min_len)

        pa = np.array(traj_a[idx])
        pb = np.array(traj_b[idx])

        distance = np.linalg.norm(pa - pb)

        if distance < COLLISION_DISTANCE_KM:
            hits += 1

    return hits / samples


def total_risk(target, all_objects):
    """
    Computes total collision risk for one satellite against all others.

    target: {"name": str, "traj": list}
    all_objects: list of same dicts
    """
    risks = []

    for other in all_objects:
        if other is target:
            continue

        p = collision_probability(target["traj"], other["traj"])

        if p > 0:
            risks.append({
                "name": other["name"],
                "probability": round(p, 6)
            })

    # Sort highest risk first
    risks.sort(key=lambda x: x["probability"], reverse=True)

    total_score = round(sum(r["probability"] for r in risks), 6)

    return total_score, risks[:5]
