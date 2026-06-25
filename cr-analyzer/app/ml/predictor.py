"""
Predictor module.

Right now: heuristic win rate + static matchup table.
Phase 2: swap predict_win_rate() for XGBoost / LightGBM model loaded from disk.
Phase 3: swap get_matchups() for matrix factorization query.

The router interface stays identical — only this file changes.
"""

from typing import Dict, Any


async def predict_win_rate(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Placeholder win rate prediction.
    Returns a score based on deck features until real model is trained.
    """
    strength = features.get("cycle_score", 50)
    offense = min(100, len(features.get("win_conditions", [])) * 30 + 40)
    raw = (strength * 0.4 + offense * 0.6)

    # Normalise to a realistic ladder win rate range (45–70%)
    win_rate = 45 + (raw / 100) * 25

    return {
        "win_rate": round(win_rate, 1),
        "confidence": "low",           # upgrades to "high" once model is trained
        "model_version": "heuristic-v0",
        "note": "Heuristic estimate. Connect battle data to train real model.",
    }


async def get_matchups(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Placeholder matchup data.
    Phase 2: query matrix factorization model for real matchup win rates.
    """
    is_cycle = features.get("is_cycle_deck", False)
    is_beatdown = features.get("is_beatdown", False)

    if is_cycle:
        counters = [
            {"archetype": "Lava Hound Balloon", "win_rate_delta": -11, "reason": "Air units bypass cycle defenses"},
            {"archetype": "Miner Poison",        "win_rate_delta": -5,  "reason": "Chip damage races your cycle"},
        ]
        favourable = [
            {"archetype": "Hog Rider cycle",   "win_rate_delta": +9,  "reason": "Mirror matchup — you cycle faster"},
            {"archetype": "Giant beatdown",     "win_rate_delta": +7,  "reason": "Out-cycle their slow pushes"},
        ]
    elif is_beatdown:
        counters = [
            {"archetype": "X-Bow siege",    "win_rate_delta": -8,  "reason": "Kites your tank indefinitely"},
            {"archetype": "Miner Poison",   "win_rate_delta": -6,  "reason": "Chip kills beatdown support"},
        ]
        favourable = [
            {"archetype": "Goblin Barrel",  "win_rate_delta": +8,  "reason": "Beatdown overwhelms chip decks"},
            {"archetype": "Hog cycle",      "win_rate_delta": +5,  "reason": "Tank absorbs Hog pressure"},
        ]
    else:
        counters = [
            {"archetype": "Lava Hound",  "win_rate_delta": -7, "reason": "Air coverage gap"},
            {"archetype": "Siege decks", "win_rate_delta": -5, "reason": "Limited ranged answer"},
        ]
        favourable = [
            {"archetype": "Goblin Barrel", "win_rate_delta": +6, "reason": "Strong ground defence"},
            {"archetype": "Giant Witch",   "win_rate_delta": +4, "reason": "Spell cycle advantage"},
        ]

    return {
        "counters": counters,
        "favourable": favourable,
        "model_version": "static-v0",
        "note": "Static matchup table. Upgrades to ML after data collection.",
    }
