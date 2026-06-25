from typing import List, Dict, Any

RARITY_WEIGHTS = {
    "Common": 1,
    "Rare": 2,
    "Epic": 3,
    "Legendary": 4,
    "Champion": 5,
}

# Rough archetype tagging by card id ranges / names
# Expand this as you collect more data
WIN_CONDITIONS = {
    "goblin barrel", "hog rider", "balloon", "lava hound",
    "three musketeers", "giant", "golem", "royal giant",
    "graveyard", "miner", "x-bow", "mortar", "ram rider",
    "electro giant", "sparky", "pekka",
}

SPELLS = {
    "fireball", "lightning", "rocket", "poison", "freeze",
    "earthquake", "arrows", "zap", "log", "snowball",
    "tornado", "clone", "mirror", "rage",
}


def extract_features(cards: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not cards:
        return {}

    elixir_costs = [c.get("elixirCost", 0) for c in cards if c.get("elixirCost")]
    avg_elixir = round(sum(elixir_costs) / len(elixir_costs), 2) if elixir_costs else 0

    rarity_counts: Dict[str, int] = {}
    for c in cards:
        r = c.get("rarity", "Common")
        rarity_counts[r] = rarity_counts.get(r, 0) + 1

    names_lower = [c.get("name", "").lower() for c in cards]

    win_cons = [n for n in names_lower if n in WIN_CONDITIONS]
    spells = [n for n in names_lower if n in SPELLS]

    # Cycle speed: lower avg elixir = faster cycle
    cycle_score = max(0, min(100, int((5.0 - avg_elixir) / 5.0 * 100 + 50)))

    # Spell pressure: more spells = more ranged damage potential
    spell_pressure = min(100, len(spells) * 25)

    return {
        "avg_elixir": avg_elixir,
        "elixir_costs": sorted(elixir_costs),
        "rarity_distribution": rarity_counts,
        "win_conditions": win_cons,
        "spells": spells,
        "card_count": len(cards),
        "cycle_score": cycle_score,
        "spell_pressure": spell_pressure,
        "is_cycle_deck": avg_elixir <= 3.5,
        "is_beatdown": avg_elixir >= 4.5,
    }


def score_deck(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Heuristic scores 0-100. Replace with trained model outputs
    once you have battle data collected.
    """
    avg_e = features.get("avg_elixir", 3.5)
    cycle = features.get("cycle_score", 50)
    spell_p = features.get("spell_pressure", 50)
    win_con_count = len(features.get("win_conditions", []))

    # Offense: win conditions + spell pressure
    offense = min(100, win_con_count * 25 + spell_p * 0.5)

    # Defense: mid-elixir range is best for reactive play
    defense = max(0, 100 - abs(avg_e - 3.8) * 30)

    # Consistency: having exactly 1-2 win cons is most consistent
    consistency = 100 if win_con_count == 1 else (75 if win_con_count == 2 else 40)

    # Overall strength
    strength = int(offense * 0.35 + defense * 0.30 + cycle * 0.20 + consistency * 0.15)

    # Meta grade
    if strength >= 85:
        grade = "S"
    elif strength >= 75:
        grade = "A"
    elif strength >= 65:
        grade = "B"
    elif strength >= 50:
        grade = "C"
    else:
        grade = "D"

    return {
        "offense": round(offense),
        "defense": round(defense),
        "cycle": cycle,
        "consistency": consistency,
        "overall_strength": strength,
        "meta_grade": grade,
    }
