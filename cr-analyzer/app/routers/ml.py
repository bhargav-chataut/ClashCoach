from fastapi import APIRouter, HTTPException
from app.ml.deck_features import extract_features, score_deck
from app.ml.predictor import predict_win_rate, get_matchups

router = APIRouter()


@router.post("/analyze-deck")
async def analyze_deck_ml(payload: dict):
    """
    Full ML analysis: win rate prediction + deck scores + matchups.
    Body: { "cards": [...] }
    """
    cards = payload.get("cards", [])
    if not cards:
        raise HTTPException(400, "cards list is required")

    features = extract_features(cards)
    scores = score_deck(features)
    win_rate = await predict_win_rate(features)
    matchups = await get_matchups(features)

    return {
        "features": features,
        "scores": scores,
        "win_rate_prediction": win_rate,
        "matchups": matchups,
    }


@router.post("/matchups")
async def get_deck_matchups(payload: dict):
    """Return top counter decks and favourable matchups."""
    cards = payload.get("cards", [])
    if not cards:
        raise HTTPException(400, "cards list is required")
    features = extract_features(cards)
    return await get_matchups(features)
