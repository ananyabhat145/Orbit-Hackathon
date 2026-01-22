import numpy as np

COLLISION_DISTANCE_KM = 1.0  # conservative conjunction threshold


def collision_probability(traj_a, traj_b, samples=200):
    """
    Monte Carlo probability of close approach.
    """
    if not traj_a or not traj_b:
        return 0.0

    min_len = min(len(traj_a), len(traj_b))
    hits = 0

    for _ in range(samples):
        idx = np.random.randint(0, min_len)
        pa = traj_a[idx]["pos"]
        pb = traj_b[idx]["pos"]

        dist = np.linalg.norm(pa - pb)
        if dist < COLLISION_DISTANCE_KM:
            hits += 1

    return hits / samples


def total_risk(target_traj, all_trajs):
    risks = []

    for other in all_trajs:
        if other is target_traj:
            continue

        p = collision_probability(target_traj["traj"], other["traj"])
        if p > 0:
            risks.append({
                "name": other["name"],
                "probability": p
            })

    risks.sort(key=lambda x: x["probability"], reverse=True)
    total = sum(r["probability"] for r in risks)

    return total, risks[:5]

