const RARITY_COLORS = {
  common:    "#888",
  rare:      "#378ADD",
  epic:      "#9b6dff",
  legendary: "#f0a500",
  champion:  "#f05252",
};

function CardTile({ card }) {
  const rarity = card.rarity?.toLowerCase() || "common";
  const color = RARITY_COLORS[rarity] || "#888";
  const pct = Math.round((card.level / card.maxLevel) * 100);

  return (
    <div style={{
      background: "var(--bg3)",
      border: "1px solid var(--border)",
      borderRadius: 10,
      padding: "10px 8px",
      display: "flex", flexDirection: "column",
      alignItems: "center", gap: 6,
      position: "relative", overflow: "hidden",
    }}>
      {/* rarity bar bottom */}
      <div style={{
        position: "absolute", bottom: 0, left: 0, right: 0,
        height: 3, background: color,
      }} />

      {/* card image */}
      {card.iconUrls?.medium ? (
        <img
          src={card.iconUrls.medium}
          alt={card.name}
          style={{ width: 52, height: 52, objectFit: "contain" }}
        />
      ) : (
        <div style={{
          width: 52, height: 52, borderRadius: 8,
          background: "var(--bg2)",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 22,
        }}>⚔️</div>
      )}

      <p style={{ fontSize: 11, fontWeight: 500, textAlign: "center", lineHeight: 1.2, color: "var(--text)" }}>
        {card.name}
      </p>

      <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
        <span style={{ fontSize: 10, color: "var(--text3)" }}>Lv {card.level}/{card.maxLevel}</span>
        <span style={{
          fontSize: 10, fontWeight: 600,
          background: "var(--bg2)", borderRadius: 4,
          padding: "1px 5px",
          color: card.elixirCost <= 2 ? "var(--green)" : card.elixirCost >= 6 ? "var(--red)" : "var(--accent)",
        }}>
          {card.elixirCost}💧
        </span>
      </div>

      {/* level bar */}
      <div style={{ width: "100%", height: 3, background: "var(--bg2)", borderRadius: 99 }}>
        <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: 99 }} />
      </div>
    </div>
  );
}

export default function CardGrid({ cards, features }) {
  return (
    <div className="card">
      <p className="card-title">Current deck</p>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 8, marginBottom: 16 }}>
        {cards.map((c) => <CardTile key={c.id} card={c} />)}
      </div>

      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        <span className="pill pill-blue">Avg elixir: {features.avg_elixir}</span>
        {features.is_cycle_deck && <span className="pill pill-green">Fast cycle</span>}
        {features.is_beatdown && <span className="pill pill-amber">Beatdown</span>}
        {features.win_conditions?.map(w => (
          <span key={w} className="pill pill-amber" style={{ textTransform: "capitalize" }}>{w}</span>
        ))}
        {features.spells?.map(s => (
          <span key={s} className="pill pill-blue" style={{ textTransform: "capitalize" }}>{s}</span>
        ))}
      </div>
    </div>
  );
}
