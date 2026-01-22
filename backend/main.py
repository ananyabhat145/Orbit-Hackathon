from fastapi import FastAPI
from propagate import propagate_satellite
from risk import total_risk
from explain import explain_risk
from satellites_data import satellites  # your manual satellite list

app = FastAPI(title="Debrismap Risk API")

# Precompute trajectories once at startup
TRAJECTORIES = []

for sat in satellites:
    # Update propagate_satellite to accept manual parameters
    traj = propagate_satellite(
        perigee_km=sat["perigee_km"],
        apogee_km=sat["apogee_km"],
        inclination_deg=sat["inclination_deg"],
        minutes_ahead=1440
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


