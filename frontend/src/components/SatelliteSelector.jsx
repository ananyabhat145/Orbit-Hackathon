export default function SatelliteSelector({ satellites, onSelect }) {
  return (
    <select onChange={(e) => onSelect(e.target.value)}>
      <option value="">Select a satellite</option>
      {satellites.map((sat) => (
        <option key={sat.id} value={sat.id}>
          {sat.name}
        </option>
      ))}
    </select>
  );
}
