from fastapi import APIRouter, HTTPException
from app.services import cr_client, cache

router = APIRouter()


@router.get("/{tag}")
async def get_player(tag: str):
    """Fetch player profile by tag (with or without #)."""
    cache_key = f"player:{tag.upper().lstrip('#')}"
    cached = await cache.cache_get(cache_key)
    if cached:
        return cached

    try:
        data = await cr_client.get_player(tag)
    except LookupError:
        raise HTTPException(404, f"Player {tag} not found")
    except PermissionError as e:
        raise HTTPException(403, str(e))
    except RuntimeError as e:
        raise HTTPException(503, str(e))

    await cache.cache_set(cache_key, data, ttl=300)
    return data


@router.get("/{tag}/battles")
async def get_battle_log(tag: str):
    """Fetch last 25 battles for a player."""
    cache_key = f"battles:{tag.upper().lstrip('#')}"
    cached = await cache.cache_get(cache_key)
    if cached:
        return cached

    try:
        data = await cr_client.get_battle_log(tag)
    except LookupError:
        raise HTTPException(404, f"Player {tag} not found")
    except RuntimeError as e:
        raise HTTPException(503, str(e))

    await cache.cache_set(cache_key, data, ttl=120)
    return data


@router.get("/{tag}/chests")
async def get_upcoming_chests(tag: str):
    """Fetch upcoming chest sequence."""
    try:
        return await cr_client.get_upcoming_chests(tag)
    except LookupError:
        raise HTTPException(404, f"Player {tag} not found")
    except RuntimeError as e:
        raise HTTPException(503, str(e))
