from fastapi import FastAPI
from propagate import propagate_satellite
from risk import total_risk
from explain import explain_risk
from satellites_data import satellites 

app = FastAPI(title="Debrismap Risk API")

# Precompute trajectories once at startup
TRAJECTORIES = []

for sat in satellites:
    # Compute trajectory for each satellite
    traj = propagate_satellite(
        sat["satrec"],
        sat["epoch"],
        minutes_ahead=1440  # 1 day ahead
    )
    TRAJECTORIES.append({
        "name": sat["name"],
        "traj": traj
    })


@app.get("/risk/{sat_id}")
def risk_endpoint(sat_id: int):
    if sat_id < 0 or sat_id >= len(TRAJECTORIES):
        return {"error": "Invalid satellite ID"}

    target = TRAJECTORIES[sat_id]
    total, threats = total_risk(target, TRAJECTORIES)
    explanation = explain_risk(total, threats)

    return {
        "satellite": target["name"],
        "risk_score": round(total, 4),
        "top_threats": threats,
        "explanation": explanation
    }
