# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy import select
# from sqlalchemy.orm import Session

# from ..database import get_db
# from ..models import User
# from ..schemas import (
#     TokenResponse,
#     UserRegister,
#     UserResponse,
# )
# from ..security import (
#     create_access_token,
#     get_current_user,
#     hash_password,
#     verify_password,
# )

# router = APIRouter(
#     prefix="/api/auth",
#     tags=["Authentication"],
# )


# @router.post(
#     "/register",
#     response_model=UserResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def register(
#     payload: UserRegister,
#     db: Session = Depends(get_db),
# ):
#     existing_user = db.scalar(
#         select(User).where(
#             User.email == payload.email.lower()
#         )
#     )

#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="An account with this email already exists.",
#         )

#     user = User(
#         name=payload.name.strip(),
#         email=payload.email.lower(),
#         hashed_password=hash_password(
#             payload.password
#         ),
#         state=payload.state.strip(),
#         district=payload.district.strip(),
#         area=payload.area.strip(),
#     )

#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     return user


# @router.post(
#     "/login",
#     response_model=TokenResponse,
# )
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db),
# ):
#     user = db.scalar(
#         select(User).where(
#             User.email == form_data.username.lower()
#         )
#     )

#     if (
#         user is None
#         or not verify_password(
#             form_data.password,
#             user.hashed_password,
#         )
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={
#                 "WWW-Authenticate": "Bearer"
#             },
#         )

#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="User account is inactive",
#         )

#     token = create_access_token(
#         user.id
#     )

#     return {
#         "access_token": token,
#         "token_type": "bearer",
#     }


# @router.get(
#     "/me",
#     response_model=UserResponse,
# )
# def get_me(
#     current_user: User = Depends(
#         get_current_user
#     ),
# ):
#     return current_user
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import TokenResponse, UserCreate, UserResponse
from app.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)

logger = logging.getLogger("krishimap.auth")

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize_email(email: str) -> str:
    """
    Normalize email addresses consistently across registration and login.
    """
    return email.strip().lower()


# ---------------------------------------------------------------------------
# Register
# ---------------------------------------------------------------------------

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    email = normalize_email(payload.email)

    # Check for an existing account before attempting the INSERT.
    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        name=payload.name.strip(),
        email=email,
        hashed_password=hash_password(payload.password),
        state=payload.state.strip() if payload.state else None,
        district=(
            payload.district.strip()
            if payload.district
            else None
        ),
        area=payload.area,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()

        # Protect against a race condition where another request
        # registers the same email between our SELECT and INSERT.
        logger.warning(
            "Registration conflict for email=%s",
            email,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    except Exception:
        db.rollback()

        logger.exception(
            "Unexpected error while registering user."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create account",
        )

    return user


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return an access token.

    OAuth2PasswordRequestForm is intentionally retained because the
    existing frontend sends username/password form data to this endpoint.
    """

    email = normalize_email(form_data.username)

    user = db.scalar(
        select(User).where(User.email == email)
    )

    # Do not reveal whether the email exists.
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    if not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ---------------------------------------------------------------------------
# Current authenticated user
# ---------------------------------------------------------------------------

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """
    return current_user