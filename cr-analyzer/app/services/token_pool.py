import asyncio
import time
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class TokenPool:
    """
    Round-robin token pool for CR API keys.
    Tracks rate limit hits and backs off automatically.
    Add a friend's token at runtime via add_token().
    """

    def __init__(self, tokens: List[str]):
        self._tokens = list(tokens)
        self._index = 0
        self._cooldowns: dict[str, float] = {}  # token -> cooldown_until timestamp
        self._lock = asyncio.Lock()

    async def get_token(self) -> Optional[str]:
        async with self._lock:
            now = time.time()
            available = [t for t in self._tokens if self._cooldowns.get(t, 0) < now]
            if not available:
                logger.warning("All tokens are in cooldown!")
                return None
            token = available[self._index % len(available)]
            self._index = (self._index + 1) % len(available)
            return token

    async def mark_rate_limited(self, token: str, cooldown_seconds: int = 60):
        async with self._lock:
            self._cooldowns[token] = time.time() + cooldown_seconds
            logger.warning(f"Token ...{token[-6:]} rate limited, cooling {cooldown_seconds}s")

    async def add_token(self, token: str):
        async with self._lock:
            if token not in self._tokens:
                self._tokens.append(token)
                logger.info(f"Added new token ...{token[-6:]} (pool size: {len(self._tokens)})")

    async def remove_token(self, token: str):
        async with self._lock:
            self._tokens = [t for t in self._tokens if t != token]

    @property
    def size(self) -> int:
        return len(self._tokens)


# Singleton — imported everywhere
_pool: Optional[TokenPool] = None


def get_token_pool() -> TokenPool:
    global _pool
    if _pool is None:
        from app.config import settings
        _pool = TokenPool(settings.token_list)
        logger.info(f"Token pool initialised with {_pool.size} token(s)")
    return _pool
