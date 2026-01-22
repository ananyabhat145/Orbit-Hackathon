export default function RiskCard({ risk }) {
  return (
    <div className="card">
      <h2>{risk.satellite}</h2>
      <h3>Risk Score: {risk.risk_score}</h3>
      <p>{risk.explanation}</p>
    </div>
  );
}
