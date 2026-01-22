const API_BASE = "http://localhost:8000";

export async function fetchSatellites() {
  const res = await fetch(`${API_BASE}/satellites`);
  return res.json();
}

export async function fetchRisk(id) {
  const res = await fetch(`${API_BASE}/risk/${id}`);
  return res.json();
}
