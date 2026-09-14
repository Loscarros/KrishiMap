from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Farm, FarmTask, User
from ..schemas import (
    FarmTaskCreate,
    FarmTaskResponse,
    FarmTaskUpdate,
)
from ..security import get_current_user


router = APIRouter(
    prefix="/api/farms",
    tags=["Farm Calendar"],
)


def get_owned_farm(
    farm_id: int,
    user_id: int,
    db: Session,
) -> Farm:
    farm = db.scalar(
        select(Farm).where(
            Farm.id == farm_id,
            Farm.owner_id == user_id,
        )
    )

    if farm is None:
        raise HTTPException(
            status_code=404,
            detail="Farm not found.",
        )

    return farm


@router.get(
    "/{farm_id}/tasks",
    response_model=list[FarmTaskResponse],
)
def get_tasks(
    farm_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    get_owned_farm(
        farm_id,
        current_user.id,
        db,
    )

    tasks = db.scalars(
        select(FarmTask)
        .where(
            FarmTask.farm_id == farm_id
        )
        .order_by(
            FarmTask.date.asc(),
            FarmTask.id.asc(),
        )
    ).all()

    return tasks


@router.post(
    "/{farm_id}/tasks",
    response_model=FarmTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    farm_id: int,
    payload: FarmTaskCreate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    get_owned_farm(
        farm_id,
        current_user.id,
        db,
    )

    task = FarmTask(
        farm_id=farm_id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        date=payload.date,
        type=payload.type,
        status=payload.status,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.patch(
    "/{farm_id}/tasks/{task_id}",
    response_model=FarmTaskResponse,
)
def update_task(
    farm_id: int,
    task_id: int,
    payload: FarmTaskUpdate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    get_owned_farm(
        farm_id,
        current_user.id,
        db,
    )

    task = db.scalar(
        select(FarmTask).where(
            FarmTask.id == task_id,
            FarmTask.farm_id == farm_id,
        )
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    if payload.title is not None:
        task.title = payload.title.strip()

    if payload.description is not None:
        task.description = (
            payload.description.strip()
        )

    if payload.date is not None:
        task.date = payload.date

    if payload.type is not None:
        task.type = payload.type

    if payload.status is not None:
        task.status = payload.status

    db.commit()
    db.refresh(task)

    return task


@router.delete(
    "/{farm_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    farm_id: int,
    task_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    get_owned_farm(
        farm_id,
        current_user.id,
        db,
    )

    task = db.scalar(
        select(FarmTask).where(
            FarmTask.id == task_id,
            FarmTask.farm_id == farm_id,
        )
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    db.delete(task)
    db.commit()

    return None