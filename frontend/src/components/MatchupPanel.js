export default function MatchupPanel({ matchups }) {
  if (!matchups) return null;

  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>

      <div className="card">
        <p className="card-title">⚠️ Counters you</p>
        {matchups.counters?.map((m, i) => (
          <div key={i} style={{
            display: "flex", alignItems: "center", justifyContent: "space-between",
            padding: "10px 0",
            borderBottom: i < matchups.counters.length - 1 ? "1px solid var(--border)" : "none",
          }}>
            <div>
              <p style={{ fontSize: 14, fontWeight: 500 }}>{m.archetype}</p>
              <p style={{ fontSize: 12, color: "var(--text2)", marginTop: 2 }}>{m.reason}</p>
            </div>
            <span className="pill pill-red">{m.win_rate_delta}% WR</span>
          </div>
        ))}
      </div>

      <div className="card">
        <p className="card-title">✅ Favourable matchups</p>
        {matchups.favourable?.map((m, i) => (
          <div key={i} style={{
            display: "flex", alignItems: "center", justifyContent: "space-between",
            padding: "10px 0",
            borderBottom: i < matchups.favourable.length - 1 ? "1px solid var(--border)" : "none",
          }}>
            <div>
              <p style={{ fontSize: 14, fontWeight: 500 }}>{m.archetype}</p>
              <p style={{ fontSize: 12, color: "var(--text2)", marginTop: 2 }}>{m.reason}</p>
            </div>
            <span className="pill pill-green">+{m.win_rate_delta}% WR</span>
          </div>
        ))}
      </div>

    </div>
  );
}
