import { useEffect, useState } from "react";
import axios from "axios";
import CardGrid from "../components/CardGrid";
import ScorePanel from "../components/ScorePanel";
import MatchupPanel from "../components/MatchupPanel";

const API = process.env.REACT_APP_API_URL || "https://clashcoach.onrender.com";

export default function DeckAnalyzer({ tag }) {
  const [player, setPlayer]   = useState(null);
  const [deck, setDeck]       = useState(null);
  const [ml, setMl]           = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState(null);

  useEffect(() => {
    setLoading(true); setError(null);
    setPlayer(null); setDeck(null); setMl(null);

    const cleanTag = tag.replace("#", "");

    Promise.all([
      axios.get(`${API}/api/players/${cleanTag}`),
      axios.get(`${API}/api/decks/${cleanTag}/current`),
    ])
      .then(async ([pRes, dRes]) => {
        setPlayer(pRes.data);
        setDeck(dRes.data);
        // ML analysis
        const mlRes = await axios.post(`${API}/api/ml/analyze-deck`, {
          cards: dRes.data.cards,
        });
        setMl(mlRes.data);
      })
      .catch((e) => setError(e.response?.data?.detail || "Failed to load player data"))
      .finally(() => setLoading(false));
  }, [tag]);

  if (loading) return (
    <div className="loading">
      <div className="spinner" />
      <p>Analyzing #{tag}...</p>
    </div>
  );

  if (error) return (
    <div className="error-box" style={{ marginTop: 40 }}>
      <p style={{ fontSize: 18, fontWeight: 600 }}>Could not load player</p>
      <p style={{ marginTop: 8, opacity: 0.8 }}>{error}</p>
    </div>
  );

  const scores = deck?.scores || {};
  const features = deck?.features || {};

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>

      {/* Player header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 12 }}>
        <div>
          <h2 style={{ fontSize: 26, fontWeight: 700, fontFamily: "'Barlow Condensed', sans-serif", letterSpacing: "0.01em" }}>
            {player?.name}
            <span style={{ marginLeft: 12, fontSize: 14, fontWeight: 500, color: "var(--text3)", fontFamily: "Inter" }}>#{tag}</span>
          </h2>
          <p style={{ color: "var(--text2)", fontSize: 14, marginTop: 4 }}>
            {player?.arena?.name} · {player?.trophies?.toLocaleString()} trophies · Best: {player?.bestTrophies?.toLocaleString()}
          </p>
        </div>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <span className="pill pill-blue">W {player?.wins}</span>
          <span className="pill pill-red">L {player?.losses}</span>
          <span className={`pill ${player?.currentWinLoseStreak > 0 ? "pill-green" : "pill-red"}`}>
            Streak {player?.currentWinLoseStreak > 0 ? "+" : ""}{player?.currentWinLoseStreak}
          </span>
        </div>
      </div>

      {/* Main grid */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <CardGrid cards={deck?.cards || []} features={features} />
        <ScorePanel scores={scores} features={features} ml={ml} />
      </div>

      <MatchupPanel matchups={ml?.matchups} />
    </div>
  );
}
