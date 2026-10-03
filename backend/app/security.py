# import os
# from datetime import datetime, timedelta, timezone

# import jwt
# from dotenv import load_dotenv
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from pwdlib import PasswordHash
# from sqlalchemy.orm import Session

# from .database import get_db
# from .models import User

# load_dotenv()

# SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# if not SECRET_KEY:
#     raise RuntimeError(
#         "JWT_SECRET_KEY is not configured"
#     )

# ALGORITHM = os.getenv(
#     "JWT_ALGORITHM",
#     "HS256",
# )

# ACCESS_TOKEN_EXPIRE_MINUTES = int(
#     os.getenv(
#         "ACCESS_TOKEN_EXPIRE_MINUTES",
#         "10080",
#     )
# )

# password_hash = PasswordHash.recommended()

# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/api/auth/login",
# )


# def hash_password(password: str) -> str:
#     return password_hash.hash(password)


# def verify_password(
#     plain_password: str,
#     hashed_password: str,
# ) -> bool:
#     return password_hash.verify(
#         plain_password,
#         hashed_password,
#     )


# def create_access_token(
#     user_id: int,
# ) -> str:
#     expires = datetime.now(
#         timezone.utc
#     ) + timedelta(
#         minutes=ACCESS_TOKEN_EXPIRE_MINUTES
#     )

#     payload = {
#         "sub": str(user_id),
#         "exp": expires,
#     }

#     return jwt.encode(
#         payload,
#         SECRET_KEY,
#         algorithm=ALGORITHM,
#     )


# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db),
# ) -> User:

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={
#             "WWW-Authenticate": "Bearer"
#         },
#     )

#     try:
#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM],
#         )

#         user_id = payload.get("sub")

#         if user_id is None:
#             raise credentials_exception

#         user_id = int(user_id)

#     except (
#         jwt.InvalidTokenError,
#         ValueError,
#         TypeError,
#     ):
#         raise credentials_exception

#     user = db.get(User, user_id)

#     if user is None:
#         raise credentials_exception

#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="User account is inactive",
#         )

#     return user

import logging
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User


# ============================================================================
# ENVIRONMENT
# ============================================================================

load_dotenv()


# ============================================================================
# LOGGING
# ============================================================================

logger = logging.getLogger("krishimap.security")


# ============================================================================
# JWT CONFIGURATION
# ============================================================================

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not JWT_SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY environment variable is not configured."
    )


JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256",
)


# Keep the existing 7-day default so the frontend authentication
# behavior does not change unexpectedly.
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "10080",
    )
)


# ============================================================================
# PASSWORD HASHING
# ============================================================================

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using pwdlib's recommended
    password hashing configuration.
    """

    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against a stored password hash.

    Invalid/corrupt hashes are treated as failed authentication
    rather than being allowed to crash the request.
    """

    try:
        return password_hash.verify(
            plain_password,
            hashed_password,
        )

    except Exception:
        logger.exception(
            "Password verification failed."
        )

        return False


# ============================================================================
# OAUTH2
# ============================================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
)


# ============================================================================
# JWT CREATION
# ============================================================================

def create_access_token(
    user_id: int,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a JWT access token.

    Existing frontend-compatible claims are preserved:

        sub -> user ID
        exp -> expiration timestamp

    `iat` is additionally included as token issuance time.
    """

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    now = datetime.now(timezone.utc)

    expire = now + expires_delta

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": now,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


# ============================================================================
# AUTHENTICATION ERROR
# ============================================================================

def _credentials_exception() -> HTTPException:
    """
    Return the standard authentication failure response.

    A consistent response avoids exposing whether a token was malformed,
    expired, or otherwise invalid.
    """

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )


# ============================================================================
# CURRENT USER
# ============================================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Decode the JWT and return the authenticated user.

    Authentication failures return 401.

    Inactive users return 403.
    """

    credentials_exception = _credentials_exception()

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        subject = payload.get("sub")

        if subject is None:
            raise credentials_exception

        try:
            user_id = int(subject)

        except (TypeError, ValueError):
            raise credentials_exception

        if user_id <= 0:
            raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected JWT validation error."
        )

        raise credentials_exception

    user = db.scalar(
        select(User).where(
            User.id == user_id,
        )
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user