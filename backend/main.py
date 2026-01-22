from fastapi import FastAPI, HTTPException
from propagate import propagate_satellite
from risk import total_risk
from explain import explain_risk
from satellites_data import satellites

app = FastAPI(title="Debrismap Risk API")

TRAJECTORIES = []


@app.on_event("startup")
def preload_trajectories():
    """
    Precompute trajectories using manually defined state vectors.
    """
    global TRAJECTORIES
    TRAJECTORIES = []

    for sat in satellites:
        traj = propagate_satellite(
            position=sat["position"],
            velocity=sat["velocity"],
            minutes_ahead=1440
        )

        TRAJECTORIES.append({
            "name": sat["name"],
            "traj": traj
        })

    print(f"[Debrismap] Loaded {len(TRAJECTORIES)} trajectories")


@app.get("/satellites")
def list_satellites():
    return [
        {"id": i, "name": t["name"]}
        for i, t in enumerate(TRAJECTORIES)
    ]


@app.get("/risk/{sat_id}")
def risk_endpoint(sat_id: int):
    if sat_id < 0 or sat_id >= len(TRAJECTORIES):
        raise HTTPException(status_code=404, detail="Satellite not found")

    target = TRAJECTORIES[sat_id]

    others = [
        t for i, t in enumerate(TRAJECTORIES)
        if i != sat_id
    ]

    total, threats = total_risk(target, others)
    explanation = explain_risk(total, threats)

    return {
        "satellite": target["name"],
        "risk_score": round(total, 4),
        "top_threats": threats[:5],
        "explanation": explanation
    }
