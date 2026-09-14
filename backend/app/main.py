from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine

from .routers import (
    auth,
    users,
    weather,
    recommendations,
    farms,
    tasks,
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="KrishiMap AI API",
    description="AI Farm Intelligence Backend",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth.router
)

app.include_router(
    users.router
)

app.include_router(
    weather.router
)

app.include_router(
    recommendations.router
)

app.include_router(
    farms.router
)

app.include_router(
    tasks.router
)


@app.get("/")
def root():
    return {
        "message": "KrishiMap AI API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }