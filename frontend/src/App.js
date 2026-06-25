import { useState } from "react";
import DeckAnalyzer from "./pages/DeckAnalyzer";
import "./App.css";

export default function App() {
  const [tag, setTag] = useState("");
  const [submitted, setSubmitted] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (tag.trim()) setSubmitted(tag.trim().replace("#", ""));
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">⚔️</span>
            <span className="logo-text">ClashCoach</span>
            <span className="logo-badge">AI</span>
          </div>
          <form className="search-form" onSubmit={handleSubmit}>
            <input
              className="tag-input"
              placeholder="Enter player tag e.g. PJ2G8ULQU"
              value={tag}
              onChange={(e) => setTag(e.target.value)}
            />
            <button className="search-btn" type="submit">Analyze</button>
          </form>
        </div>
      </header>

      <main className="main">
        {!submitted ? (
          <div className="hero">
            <h1 className="hero-title">Know your deck.<br />Own the ladder.</h1>
            <p className="hero-sub">
              AI-powered deck analysis, win rate prediction, and matchup insights
              for serious Clash Royale players.
            </p>
            <form className="hero-form" onSubmit={handleSubmit}>
              <input
                className="hero-input"
                placeholder="#PJ2G8ULQU"
                value={tag}
                onChange={(e) => setTag(e.target.value)}
              />
              <button className="hero-btn" type="submit">Get Your Analysis →</button>
            </form>
          </div>
        ) : (
          <DeckAnalyzer tag={submitted} />
        )}
      </main>
    </div>
  );
}
