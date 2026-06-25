import httpx
import logging
from urllib.parse import quote

from app.config import settings
from app.services.token_pool import get_token_pool

logger = logging.getLogger(__name__)

BASE = settings.cr_api_base_url


def _encode_tag(tag: str) -> str:
    """CR tags start with #, must be URL-encoded as %23."""
    tag = tag.strip().upper()
    if not tag.startswith("#"):
        tag = "#" + tag
    return quote(tag, safe="")


async def _get(path: str) -> dict:
    pool = get_token_pool()
    token = await pool.get_token()
    if not token:
        raise RuntimeError("No available API tokens")

    url = f"{BASE}{path}"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, headers=headers)

    if resp.status_code == 429:
        await pool.mark_rate_limited(token)
        raise RuntimeError("Rate limited — try again shortly")

    if resp.status_code == 403:
        raise PermissionError(f"Token rejected for {path}")

    if resp.status_code == 404:
        raise LookupError(f"Not found: {path}")

    resp.raise_for_status()
    return resp.json()


async def get_player(tag: str) -> dict:
    return await _get(f"/players/{_encode_tag(tag)}")


async def get_battle_log(tag: str) -> list:
    data = await _get(f"/players/{_encode_tag(tag)}/battlelog")
    return data if isinstance(data, list) else data.get("items", [])


async def get_upcoming_chests(tag: str) -> dict:
    return await _get(f"/players/{_encode_tag(tag)}/upcomingchests")


async def get_cards() -> dict:
    return await _get("/cards")
