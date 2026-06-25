from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from app.services.token_pool import get_token_pool
from app.config import settings

router = APIRouter()


class TokenPayload(BaseModel):
    token: str
    label: str = ""          # optional friendly name e.g. "Rahul's token"


@router.post("/tokens/add")
async def add_token(payload: TokenPayload):
    """
    Add a friend's CR API token to the pool at runtime.
    No restart needed.
    """
    if not payload.token or len(payload.token) < 10:
        raise HTTPException(400, "Invalid token")

    pool = get_token_pool()
    await pool.add_token(payload.token)
    return {"status": "added", "pool_size": pool.size, "label": payload.label}


@router.get("/tokens/status")
async def token_status():
    """How many tokens are in the pool."""
    pool = get_token_pool()
    return {"pool_size": pool.size}
