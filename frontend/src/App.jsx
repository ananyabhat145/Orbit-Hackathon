import { useEffect, useState } from "react";
import { fetchSatellites, fetchRisk } from "./api";
import SatelliteSelector from "./components/SatelliteSelector";
import RiskCard from "./components/RiskCard";
import ThreatList from "./components/ThreatList";

export default function App() {
  const [satellites, setSatellites] = useState([]);
  const [risk, setRisk] = useState(null);

  useEffect(() => {
    fetchSatellites().then(setSatellites);
  }, []);

  const handleSelect = async (id) => {
    if (id === "") return;
    const data = await fetchRisk(id);
    setRisk(data);
  };

  return (
    <div className="app">
      <h1>🛰️ Debrismap</h1>
      <p className="subtitle">
        Visualizing satellite collision risk in low Earth orbit
      </p>

      <SatelliteSelector satellites={satellites} onSelect={handleSelect} />

      {risk && (
        <>
          <RiskCard risk={risk} />
          <ThreatList threats={risk.top_threats} />
        </>
      )}
    </div>
  );
}
