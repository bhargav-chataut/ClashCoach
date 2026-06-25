from fastapi import APIRouter, HTTPException
from app.services import cr_client, cache
from app.ml.deck_features import extract_features, score_deck

router = APIRouter()


@router.get("/{tag}/current")
async def get_current_deck(tag: str):
    """Return the player's current deck with basic stats."""
    cache_key = f"deck:{tag.upper().lstrip('#')}"
    cached = await cache.cache_get(cache_key)
    if cached:
        return cached

    try:
        player = await cr_client.get_player(tag)
    except LookupError:
        raise HTTPException(404, f"Player {tag} not found")
    except RuntimeError as e:
        raise HTTPException(503, str(e))

    cards = player.get("currentDeck", [])
    if not cards:
        raise HTTPException(404, "No current deck found for this player")

    features = extract_features(cards)
    scores = score_deck(features)

    result = {
        "tag": player.get("tag"),
        "name": player.get("name"),
        "trophies": player.get("trophies"),
        "cards": cards,
        "features": features,
        "scores": scores,
    }

    await cache.cache_set(cache_key, result, ttl=300)
    return result


@router.post("/analyze")
async def analyze_deck(payload: dict):
    """
    Analyze an arbitrary deck passed as a list of card objects.
    Body: { "cards": [ { "id": ..., "name": ..., "elixirCost": ... } ] }
    """
    cards = payload.get("cards", [])
    if len(cards) != 8:
        raise HTTPException(400, "A deck must contain exactly 8 cards")

    features = extract_features(cards)
    scores = score_deck(features)
    return {"features": features, "scores": scores}
