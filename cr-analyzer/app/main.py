from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routers import players, decks, ml, admin
from app.services.token_pool import TokenPool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CR Analyzer API...")
    yield
    logger.info("Shutting down CR Analyzer API...")


app = FastAPI(
    title="CR Analyzer API",
    description="Clash Royale deck analyzer with ML-powered insights",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router, prefix="/api/players", tags=["players"])
app.include_router(decks.router,   prefix="/api/decks",   tags=["decks"])
app.include_router(ml.router,      prefix="/api/ml",      tags=["ml"])
app.include_router(admin.router,   prefix="/api/admin",   tags=["admin"])


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
