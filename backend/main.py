from fastapi import FastAPI, HTTPException
from propagate import propagate_satellite
from risk import total_risk
from explain import explain_risk
from satellites_data import satellites
from orbit_utils import orbital_elements_to_state_vector

app = FastAPI(title="Debrismap Risk API")

# Precomputed trajectories cache
TRAJECTORIES = []


@app.on_event("startup")
def preload_trajectories():
    """
    Precompute satellite trajectories at startup to avoid
    recalculating them on every request.
    """
    global TRAJECTORIES
    TRAJECTORIES = []

    for sat in satellites:
        # Convert simplified orbital elements to state vectors
        position, velocity = orbital_elements_to_state_vector(
            perigee_km=sat["perigee_km"],
            apogee_km=sat["apogee_km"],
            inclination_deg=sat["inclination_deg"]
        )

        # Propagate orbit forward (1 day, minute resolution)
        traj = propagate_satellite(
            position=position,
            velocity=velocity,
            minutes_ahead=1440
        )

        TRAJECTORIES.append({
            "name": sat["name"],
            "traj": traj,
            "meta": sat
        })

    print(f"[Debrismap] Loaded {len(TRAJECTORIES)} trajectories")


@app.get("/")
def root():
    """
    Health check endpoint.
    """
    return {
        "status": "Debrismap API is live 🚀",
        "satellites_loaded": len(TRAJECTORIES)
    }


@app.get("/satellites")
def list_satellites():
    """
    List available satellites and their metadata.
    """
    return [
        {
            "id": idx,
            "name": sat["name"],
            "norad": sat["meta"].get("norad"),
            "orbit": sat["meta"].get("class_of_orbit"),
            "purpose": sat["meta"].get("purpose")
        }
        for idx, sat in enumerate(TRAJECTORIES)
    ]


@app.get("/risk/{sat_id}")
def risk_endpoint(sat_id: int):
    """
    Compute conjunction risk for a given satellite
    against all others in the dataset.
    """
    if sat_id < 0 or sat_id >= len(TRAJECTORIES):
        raise HTTPException(
            status_code=404,
            detail="Invalid satellite ID"
        )

    target = TRAJECTORIES[sat_id]

    total, threats = total_risk(target, TRAJECTORIES)
    explanation = explain_risk(total, threats)

    return {
        "satellite": target["name"],
        "risk_score": total,
        "top_threats": threats,
        "explanation": explanation
    }
