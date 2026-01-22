from fastapi import FastAPI, HTTPException
from propagate import propagate_satellite
from risk import total_risk
from explain import explain_risk
from satellites_data import satellites
from orbit_utils import orbital_elements_to_state_vector

app = FastAPI(title="Debrismap Risk API")

TRAJECTORIES = []


@app.on_event("startup")
def preload_trajectories():
    global TRAJECTORIES
    TRAJECTORIES = []

    for sat in satellites:
        position, velocity = orbital_elements_to_state_vector(
            perigee_km=sat["perigee_km"],
            apogee_km=sat["apogee_km"],
            inclination_deg=sat["inclination_deg"]
        )

        traj = propagate_satellite(
            position=position,
            velocity=velocity,
            minutes_ahead=1440
        )

        TRAJECTORIES.append({
            "name": sat["name"],
            "traj": traj,
            "meta": sat  # keep metadata for explanations later
        })

    print(f"[Debrismap] Loaded {len(TRAJECTORIES)} trajectories")
