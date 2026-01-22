export default function ThreatList({ threats }) {
  if (!threats || threats.length === 0) {
    return (
      <div className="card">
        <p>No significant conjunction threats detected.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3>Top Threats</h3>
      <ul>
        {threats.map((t, i) => (
          <li key={i}>
            <strong>{t.name}</strong> — score {t.probability}
          </li>
        ))}
      </ul>
    </div>
  );
}
