# CR Analyzer

Clash Royale deck analyzer — FastAPI + Redis + Postgres + ML pipeline.

## Quick start

### 1. Get a CR API token
Go to https://developer.clashroyale.com → create an app → whitelist your IP → copy the token.

### 2. Set up your environment
```bash
cp .env.example .env
# Edit .env and paste your token into CR_API_TOKENS
```

### 3. Run
```bash
docker compose up --build
```

API is live at http://localhost:8000
Interactive docs at http://localhost:8000/docs

---

## Key endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/players/{tag}` | Player profile |
| GET | `/api/players/{tag}/battles` | Last 25 battles |
| GET | `/api/decks/{tag}/current` | Current deck + scores |
| POST | `/api/decks/analyze` | Analyze any deck |
| POST | `/api/ml/analyze-deck` | Full ML analysis |
| POST | `/api/ml/matchups` | Counter matchups |
| POST | `/api/admin/tokens/add` | Add a friend's token |
| GET | `/api/admin/tokens/status` | Token pool size |
| GET | `/health` | Health check |

---

## Adding a friend's token (no restart needed)

```bash
curl -X POST http://localhost:8000/api/admin/tokens/add \
  -H "Content-Type: application/json" \
  -d '{"token": "eyJ...", "label": "Rahul token"}'
```

---

## Project structure

```
cr-analyzer/
├── app/
│   ├── main.py           # FastAPI app + middleware
│   ├── config.py         # Settings from .env
│   ├── routers/
│   │   ├── players.py    # Player profile + battles
│   │   ├── decks.py      # Deck analysis
│   │   ├── ml.py         # ML inference endpoints
│   │   └── admin.py      # Token pool management
│   ├── services/
│   │   ├── cr_client.py  # CR API HTTP client
│   │   ├── token_pool.py # Round-robin token manager
│   │   └── cache.py      # Redis cache helpers
│   └── ml/
│       ├── deck_features.py  # Feature engineering
│       └── predictor.py      # Win rate + matchup (heuristic → ML)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## ML upgrade path

The `app/ml/predictor.py` module is a clean swap point:

1. Collect battle data via `/api/players/{tag}/battles` → store in Postgres
2. Run feature engineering on collected battles
3. Train XGBoost model on `(deck_features, opponent_deck_features) → win/loss`
4. Export model to `app/ml/models/win_predictor.pkl`
5. Replace `predict_win_rate()` to load and call the model

The router interface doesn't change — only the predictor internals.
