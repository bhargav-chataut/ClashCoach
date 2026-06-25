const BAR_COLORS = {
  offense:     "#f05252",
  defense:     "#5b8fff",
  cycle:       "#9b6dff",
  consistency: "#f0a500",
};

function StatBar({ label, value, color }) {
  return (
    <div className="stat-row">
      <span className="stat-label">{label}</span>
      <div className="stat-bar-bg">
        <div className="stat-bar-fill" style={{ width: `${value}%`, background: color }} />
      </div>
      <span className="stat-val">{value}</span>
    </div>
  );
}

export default function ScorePanel({ scores, features, ml }) {
  const grade = scores.meta_grade || "C";
  const winRate = ml?.win_rate_prediction?.win_rate;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>

      {/* Top metrics */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        <div className="card" style={{ textAlign: "center" }}>
          <p className="card-title">Win rate</p>
          <p style={{ fontSize: 28, fontWeight: 600, color: "var(--green)" }}>
            {winRate ? `${winRate}%` : "—"}
          </p>
          <p style={{ fontSize: 11, color: "var(--text3)", marginTop: 4 }}>
            {ml?.win_rate_prediction?.model_version || ""}
          </p>
        </div>
        <div className="card" style={{ textAlign: "center" }}>
          <p className="card-title">Meta grade</p>
          <p style={{ fontSize: 42, fontWeight: 700, fontFamily: "'Barlow Condensed', sans-serif" }}
             className={`grade-${grade}`}>
            {grade}
          </p>
        </div>
        <div className="card" style={{ textAlign: "center" }}>
          <p className="card-title">Deck strength</p>
          <p style={{ fontSize: 28, fontWeight: 600 }}>{scores.overall_strength}</p>
        </div>
        <div className="card" style={{ textAlign: "center" }}>
          <p className="card-title">Cycle score</p>
          <p style={{ fontSize: 28, fontWeight: 600, color: "var(--purple)" }}>{scores.cycle}</p>
        </div>
      </div>

      {/* Stat bars */}
      <div className="card">
        <p className="card-title">Attribute breakdown</p>
        <StatBar label="Offense"     value={scores.offense}     color={BAR_COLORS.offense} />
        <StatBar label="Defense"     value={scores.defense}     color={BAR_COLORS.defense} />
        <StatBar label="Cycle"       value={scores.cycle}       color={BAR_COLORS.cycle} />
        <StatBar label="Consistency" value={scores.consistency} color={BAR_COLORS.consistency} />
      </div>

    </div>
  );
}
