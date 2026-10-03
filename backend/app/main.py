# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from .database import Base, engine

# from .routers import (
#     auth,
#     users,
#     weather,
#     recommendations,
#     farms,
#     tasks,
# )


# Base.metadata.create_all(
#     bind=engine
# )


# app = FastAPI(
#     title="KrishiMap AI API",
#     description="AI Farm Intelligence Backend",
#     version="1.0.0",
# )


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# app.include_router(
#     auth.router
# )

# app.include_router(
#     users.router
# )

# app.include_router(
#     weather.router
# )

# app.include_router(
#     recommendations.router
# )

# app.include_router(
#     farms.router
# )

# app.include_router(
#     tasks.router
# )


# @app.get("/")
# def root():
#     return {
#         "message": "KrishiMap AI API is running"
#     }


# @app.get("/health")
# def health():
#     return {
#         "status": "healthy"
#     }
import logging
import os
from contextlib import asynccontextmanager

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .database import SessionLocal

# Routers
from .routers import auth, farms, recommendations, tasks, users, weather


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# LOGGING
# ============================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger("krishimap")


# ============================================================
# CORS
# ============================================================

def get_cors_origins() -> list[str]:
    """
    Read allowed frontend origins from CORS_ORIGINS.

    Example:
        CORS_ORIGINS=http://localhost:3000,https://krishimap.example.com

    Keeping localhost:3000 as the default preserves the current
    development frontend behavior.
    """
    raw_origins = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000",
    )

    origins = [
        origin.strip()
        for origin in raw_origins.split(",")
        if origin.strip()
    ]

    return origins


CORS_ORIGINS = get_cors_origins()


# ============================================================
# APPLICATION LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup/shutdown lifecycle.

    A single reusable AsyncClient is created for outbound HTTP
    requests instead of creating a new httpx client for every
    weather request.

    The client is stored on app.state and can be accessed by
    services through request dependencies.
    """

    logger.info("Starting KrishiMap API...")

    http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=5.0,
            read=10.0,
            write=10.0,
            pool=5.0,
        ),
        limits=httpx.Limits(
            max_connections=100,
            max_keepalive_connections=20,
            keepalive_expiry=30.0,
        ),
        follow_redirects=True,
        headers={
            "User-Agent": "KrishiMap-AI/1.0",
        },
    )

    app.state.http_client = http_client

    try:
        yield

    finally:
        logger.info("Shutting down KrishiMap API...")

        await http_client.aclose()

        logger.info("HTTP client closed.")


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="KrishiMap AI API",
    description="AI-powered agricultural mapping and crop recommendation API",
    version=os.getenv("APP_VERSION", "1.0.0"),
    lifespan=lifespan,
)


# ============================================================
# CORS MIDDLEWARE
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(farms.router)
app.include_router(tasks.router)
app.include_router(weather.router)
app.include_router(recommendations.router)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def root():
    return {
        "message": "KrishiMap AI API is running",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():
    """
    Existing frontend-compatible health endpoint.

    DO NOT change this response structure because it may already
    be consumed by the frontend or deployment configuration.
    """
    return {
        "status": "healthy",
    }


# ============================================================
# READINESS CHECK
# ============================================================

@app.get("/ready")
def readiness():
    """
    Readiness endpoint.

    Unlike /health, this verifies that the application can
    communicate with PostgreSQL.

    Useful for:
        - Docker
        - Kubernetes
        - Render
        - Railway
        - Fly.io
        - load balancers
        - deployment health checks
    """

    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "database": "connected",
        }

    except Exception:
        logger.exception("Readiness check failed.")

        return {
            "status": "not_ready",
            "database": "unavailable",
        }

    finally:
        db.close()