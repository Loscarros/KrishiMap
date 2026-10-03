# from datetime import datetime, timezone

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from ..database import get_db
# from ..models import User
# from ..schemas import (
#     LocationResponse,
#     LocationUpdate,
#     UserResponse,
# )
# from ..security import get_current_user

# router = APIRouter(
#     prefix="/api/users",
#     tags=["Users"],
# )


# @router.patch(
#     "/me/location",
#     response_model=LocationResponse,
# )
# def update_location(
#     payload: LocationUpdate,
#     current_user: User = Depends(
#         get_current_user
#     ),
#     db: Session = Depends(get_db),
# ):
#     current_user.latitude = payload.latitude
#     current_user.longitude = payload.longitude

#     current_user.location_updated_at = (
#         datetime.now(timezone.utc)
#     )

#     db.commit()
#     db.refresh(current_user)

#     return {
#         "latitude": current_user.latitude,
#         "longitude": current_user.longitude,
#         "location_updated_at":
#             current_user.location_updated_at,
#     }


# @router.get(
#     "/me",
#     response_model=UserResponse,
# )
# def get_profile(
#     current_user: User = Depends(
#         get_current_user
#     ),
# ):
#     return current_user

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import LocationResponse, LocationUpdate, UserResponse
from app.security import get_current_user

logger = logging.getLogger("krishimap.users")


router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


# ============================================================================
# CURRENT USER
# ============================================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


# ============================================================================
# UPDATE USER LOCATION
# ============================================================================

@router.patch(
    "/me/location",
    response_model=LocationResponse,
)
def update_location(
    payload: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the authenticated user's geographic location.

    The response contract intentionally remains:
        latitude
        longitude
        location_updated_at
    """

    # Pydantic already validates these ranges, but keeping the explicit
    # checks here provides an additional defensive layer.
    if not -90 <= payload.latitude <= 90:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Latitude must be between -90 and 90.",
        )

    if not -180 <= payload.longitude <= 180:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Longitude must be between -180 and 180.",
        )

    current_user.latitude = payload.latitude
    current_user.longitude = payload.longitude
    current_user.location_updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(current_user)

    except Exception:
        db.rollback()

        logger.exception(
            "Failed to update location for user_id=%s",
            current_user.id,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update user location.",
        )

    return {
        "latitude": current_user.latitude,
        "longitude": current_user.longitude,
        "location_updated_at": current_user.location_updated_at,
    }