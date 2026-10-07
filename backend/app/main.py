from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.api.analysis import router as analysis_router
from app.api.history import router as history_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app):
    from app.core.local_test import initialize_local_test
    await initialize_local_test()
    yield

app = FastAPI(
    title="OBSIL API",
    description="System wspomagania oceny konfliktu interesów",
    version="0.1.0-beta",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router)
app.include_router(history_router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0-beta"}
