from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import (
    LocationResponse,
    LocationUpdate,
    UserResponse,
)
from ..security import get_current_user

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.patch(
    "/me/location",
    response_model=LocationResponse,
)
def update_location(
    payload: LocationUpdate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    current_user.latitude = payload.latitude
    current_user.longitude = payload.longitude

    current_user.location_updated_at = (
        datetime.now(timezone.utc)
    )

    db.commit()
    db.refresh(current_user)

    return {
        "latitude": current_user.latitude,
        "longitude": current_user.longitude,
        "location_updated_at":
            current_user.location_updated_at,
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_profile(
    current_user: User = Depends(
        get_current_user
    ),
):
    return current_user