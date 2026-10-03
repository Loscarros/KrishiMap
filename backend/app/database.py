# import os

# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise RuntimeError("DATABASE_URL is not configured")

# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True,
# )

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )

# Base = declarative_base()


# def get_db():
#     db = SessionLocal()

#     try:
#         yield db
#     finally:
#         db.close()
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is not configured."
    )


# Connection pool settings.
#
# These are configurable through environment variables so that
# development, staging, and production can use different values.
#
# IMPORTANT:
# pool_size + max_overflow is PER APPLICATION PROCESS.
#
# Example:
#   4 workers × (pool_size=5 + max_overflow=10)
#   = potentially 60 PostgreSQL connections.
#
# Keep these values aligned with your PostgreSQL max_connections.
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "1800"))


# ============================================================
# ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=POOL_TIMEOUT,
    pool_recycle=POOL_RECYCLE,
    future=True,
)


# ============================================================
# SESSION FACTORY
# ============================================================

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ============================================================
# BASE MODEL
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():
    """
    FastAPI dependency that provides one database session
    per request.

    The session is always closed after the request finishes,
    including when an exception occurs.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()