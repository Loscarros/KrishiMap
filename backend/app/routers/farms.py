import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Farm, User
from ..schemas import (
    FarmCreate,
    FarmResponse,
)
from ..security import get_current_user


router = APIRouter(
    prefix="/api/farms",
    tags=["Farms"],
)


@router.post(
    "",
    response_model=FarmResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_farm(
    payload: FarmCreate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    farm = Farm(
        owner_id=current_user.id,
        name=payload.name.strip(),
        area_acres=payload.area_acres,
        latitude=payload.latitude,
        longitude=payload.longitude,
        boundary=json.dumps(
            payload.boundary
        ),
        crop=(
            payload.crop.strip()
            if payload.crop
            else None
        ),
    )

    db.add(farm)
    db.commit()
    db.refresh(farm)

    return FarmResponse(
        id=farm.id,
        name=farm.name,
        area_acres=farm.area_acres,
        latitude=farm.latitude,
        longitude=farm.longitude,
        boundary=json.loads(
            farm.boundary
        ),
        crop=farm.crop,
    )


@router.get(
    "",
    response_model=list[FarmResponse],
)
def get_my_farms(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    farms = db.scalars(
        select(Farm)
        .where(
            Farm.owner_id == current_user.id
        )
        .order_by(Farm.created_at.desc())
    ).all()

    return [
        FarmResponse(
            id=farm.id,
            name=farm.name,
            area_acres=farm.area_acres,
            latitude=farm.latitude,
            longitude=farm.longitude,
            boundary=json.loads(
                farm.boundary
            ),
            crop=farm.crop,
        )
        for farm in farms
    ]


@router.get(
    "/{farm_id}",
    response_model=FarmResponse,
)
def get_farm(
    farm_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    farm = db.scalar(
        select(Farm).where(
            Farm.id == farm_id,
            Farm.owner_id == current_user.id,
        )
    )

    if farm is None:
        raise HTTPException(
            status_code=404,
            detail="Farm not found.",
        )

    return FarmResponse(
        id=farm.id,
        name=farm.name,
        area_acres=farm.area_acres,
        latitude=farm.latitude,
        longitude=farm.longitude,
        boundary=json.loads(
            farm.boundary
        ),
        crop=farm.crop,
    )