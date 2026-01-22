import numpy as np

# Conjunction screening threshold (km)
CONJUNCTION_DISTANCE_KM = 10.0


def collision_probability(traj_a, traj_b, samples=300):
    """
    Estimates relative conjunction likelihood between two trajectories.
    This is NOT a true physical collision probability.
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

        if distance < CONJUNCTION_DISTANCE_KM:
            hits += 1

    return hits / samples


def total_risk(target, all_objects):
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

    risks.sort(key=lambda x: x["probability"], reverse=True)

    total_score = round(sum(r["probability"] for r in risks), 6)

    return total_score, risks[:5]
