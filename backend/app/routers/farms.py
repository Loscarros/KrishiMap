# import json

# from fastapi import (
#     APIRouter,
#     Depends,
#     HTTPException,
#     status,
# )
# from sqlalchemy import select
# from sqlalchemy.orm import Session

# from ..database import get_db
# from ..models import Farm, User
# from ..schemas import (
#     FarmCreate,
#     FarmResponse,
# )
# from ..security import get_current_user


# router = APIRouter(
#     prefix="/api/farms",
#     tags=["Farms"],
# )


# @router.post(
#     "",
#     response_model=FarmResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_farm(
#     payload: FarmCreate,
#     current_user: User = Depends(
#         get_current_user
#     ),
#     db: Session = Depends(get_db),
# ):
#     farm = Farm(
#         owner_id=current_user.id,
#         name=payload.name.strip(),
#         area_acres=payload.area_acres,
#         latitude=payload.latitude,
#         longitude=payload.longitude,
#         boundary=json.dumps(
#             payload.boundary
#         ),
#         crop=(
#             payload.crop.strip()
#             if payload.crop
#             else None
#         ),
#     )

#     db.add(farm)
#     db.commit()
#     db.refresh(farm)

#     return FarmResponse(
#         id=farm.id,
#         name=farm.name,
#         area_acres=farm.area_acres,
#         latitude=farm.latitude,
#         longitude=farm.longitude,
#         boundary=json.loads(
#             farm.boundary
#         ),
#         crop=farm.crop,
#     )


# @router.get(
#     "",
#     response_model=list[FarmResponse],
# )
# def get_my_farms(
#     current_user: User = Depends(
#         get_current_user
#     ),
#     db: Session = Depends(get_db),
# ):
#     farms = db.scalars(
#         select(Farm)
#         .where(
#             Farm.owner_id == current_user.id
#         )
#         .order_by(Farm.created_at.desc())
#     ).all()

#     return [
#         FarmResponse(
#             id=farm.id,
#             name=farm.name,
#             area_acres=farm.area_acres,
#             latitude=farm.latitude,
#             longitude=farm.longitude,
#             boundary=json.loads(
#                 farm.boundary
#             ),
#             crop=farm.crop,
#         )
#         for farm in farms
#     ]


# @router.get(
#     "/{farm_id}",
#     response_model=FarmResponse,
# )
# def get_farm(
#     farm_id: int,
#     current_user: User = Depends(
#         get_current_user
#     ),
#     db: Session = Depends(get_db),
# ):
#     farm = db.scalar(
#         select(Farm).where(
#             Farm.id == farm_id,
#             Farm.owner_id == current_user.id,
#         )
#     )

#     if farm is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Farm not found.",
#         )

#     return FarmResponse(
#         id=farm.id,
#         name=farm.name,
#         area_acres=farm.area_acres,
#         latitude=farm.latitude,
#         longitude=farm.longitude,
#         boundary=json.loads(
#             farm.boundary
#         ),
#         crop=farm.crop,
#     )
import json
import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Farm, User
from app.schemas import FarmCreate, FarmResponse
from app.security import get_current_user

logger = logging.getLogger("krishimap.farms")

router = APIRouter(
    prefix="/api/farms",
    tags=["Farms"],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def serialize_farm(farm: Farm) -> FarmResponse:
    """
    Convert the database Farm model into the existing API response format.

    Farm boundaries are stored as JSON text in the database but returned
    to the frontend as the original JSON-compatible structure.
    """

    try:
        boundary: Any = json.loads(farm.boundary)

    except (TypeError, json.JSONDecodeError):
        logger.error(
            "Invalid boundary JSON found for farm_id=%s",
            farm.id,
        )

        # This should never happen for valid application-created farms.
        # Returning an empty structure is safer than crashing the API.
        boundary = {}

    return FarmResponse(
        id=farm.id,
        name=farm.name,
        area_acres=farm.area_acres,
        latitude=farm.latitude,
        longitude=farm.longitude,
        boundary=boundary,
        crop=farm.crop,
        created_at=farm.created_at,
        updated_at=farm.updated_at,
    )


def get_owned_farm(
    farm_id: int,
    current_user: User,
    db: Session,
) -> Farm:
    """
    Retrieve a farm only if it belongs to the authenticated user.
    """

    farm = db.scalar(
        select(Farm).where(
            Farm.id == farm_id,
            Farm.owner_id == current_user.id,
        )
    )

    if farm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )

    return farm


# ---------------------------------------------------------------------------
# Create farm
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=FarmResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_farm(
    payload: FarmCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new farm owned by the authenticated user.
    """

    farm_name = payload.name.strip()

    if not farm_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Farm name cannot be empty",
        )

    try:
        boundary_json = json.dumps(
            payload.boundary,
            separators=(",", ":"),
        )

    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid farm boundary",
        )

    farm = Farm(
        owner_id=current_user.id,
        name=farm_name,
        area_acres=payload.area_acres,
        latitude=payload.latitude,
        longitude=payload.longitude,
        boundary=boundary_json,
        crop=payload.crop,
    )

    db.add(farm)

    try:
        db.commit()
        db.refresh(farm)

    except IntegrityError:
        db.rollback()

        logger.exception(
            "Database integrity error while creating farm "
            "for user_id=%s",
            current_user.id,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unable to create farm",
        )

    except Exception:
        db.rollback()

        logger.exception(
            "Unexpected error while creating farm "
            "for user_id=%s",
            current_user.id,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create farm",
        )

    return serialize_farm(farm)


# ---------------------------------------------------------------------------
# List farms
# ---------------------------------------------------------------------------

@router.get(
    "",
    response_model=list[FarmResponse],
)
def get_farms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return all farms belonging to the authenticated user.

    Results are newest-first.
    """

    farms = db.scalars(
        select(Farm)
        .where(Farm.owner_id == current_user.id)
        .order_by(
            Farm.created_at.desc(),
            Farm.id.desc(),
        )
    ).all()

    return [
        serialize_farm(farm)
        for farm in farms
    ]


# ---------------------------------------------------------------------------
# Get single farm
# ---------------------------------------------------------------------------

@router.get(
    "/{farm_id}",
    response_model=FarmResponse,
)
def get_farm(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return one farm belonging to the authenticated user.
    """

    farm = get_owned_farm(
        farm_id=farm_id,
        current_user=current_user,
        db=db,
    )

    return serialize_farm(farm)


# ---------------------------------------------------------------------------
# Update farm
# ---------------------------------------------------------------------------

@router.put(
    "/{farm_id}",
    response_model=FarmResponse,
)
def update_farm(
    farm_id: int,
    payload: FarmCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update an existing farm.

    This endpoint is retained for compatibility if the frontend uses it.
    """

    farm = get_owned_farm(
        farm_id=farm_id,
        current_user=current_user,
        db=db,
    )

    farm_name = payload.name.strip()

    if not farm_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Farm name cannot be empty",
        )

    try:
        boundary_json = json.dumps(
            payload.boundary,
            separators=(",", ":"),
        )

    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid farm boundary",
        )

    farm.name = farm_name
    farm.area_acres = payload.area_acres
    farm.latitude = payload.latitude
    farm.longitude = payload.longitude
    farm.boundary = boundary_json
    farm.crop = payload.crop

    try:
        db.commit()
        db.refresh(farm)

    except Exception:
        db.rollback()

        logger.exception(
            "Unexpected error while updating farm_id=%s",
            farm_id,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update farm",
        )

    return serialize_farm(farm)