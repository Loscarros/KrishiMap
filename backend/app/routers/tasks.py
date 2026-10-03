# from fastapi import (
#     APIRouter,
#     Depends,
#     HTTPException,
#     status,
# )

# from sqlalchemy import select
# from sqlalchemy.orm import Session

# from ..database import get_db
# from ..models import Farm, FarmTask, User
# from ..schemas import (
#     FarmTaskCreate,
#     FarmTaskResponse,
#     FarmTaskUpdate,
# )
# from ..security import get_current_user


# router = APIRouter(
#     prefix="/api/farms",
#     tags=["Farm Calendar"],
# )


# def get_owned_farm(
#     farm_id: int,
#     user_id: int,
#     db: Session,
# ) -> Farm:
#     farm = db.scalar(
#         select(Farm).where(
#             Farm.id == farm_id,
#             Farm.owner_id == user_id,
#         )
#     )

#     if farm is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Farm not found.",
#         )

#     return farm


# @router.get(
#     "/{farm_id}/tasks",
#     response_model=list[FarmTaskResponse],
# )
# def get_tasks(
#     farm_id: int,
#     current_user: User = Depends(
#         get_current_user
#     ),
#     db: Session = Depends(get_db),
# ):
#     get_owned_farm(
#         farm_id,
#         current_user.id,
#         db,
#     )

#     tasks = db.scalars(
#         select(FarmTask)
#         .where(
#             FarmTask.farm_id == farm_id
#         )
#         .order_by(
#             FarmTask.date.asc(),
#             FarmTask.id.asc(),
#         )
#     ).all()

#     return tasks


# @router.post(
#     "/{farm_id}/tasks",
#     response_model=FarmTaskResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_task(
#     farm_id: int,
#     payload: FarmTaskCreate,
#     current_user: User = Depends(
#         get_current_user
#     ),
#     db: Session = Depends(get_db),
# ):
#     get_owned_farm(
#         farm_id,
#         current_user.id,
#         db,
#     )

#     task = FarmTask(
#         farm_id=farm_id,
#         title=payload.title.strip(),
#         description=payload.description.strip(),
#         date=payload.date,
#         type=payload.type,
#         status=payload.status,
#     )

#     db.add(task)
#     db.commit()
#     db.refresh(task)

#     return task


# @router.patch(
#     "/{farm_id}/tasks/{task_id}",
#     response_model=FarmTaskResponse,
# )
# def update_task(
#     farm_id: int,
#     task_id: int,
#     payload: FarmTaskUpdate,
#     current_user: User = Depends(
#         get_current_user
#     ),
#     db: Session = Depends(get_db),
# ):
#     get_owned_farm(
#         farm_id,
#         current_user.id,
#         db,
#     )

#     task = db.scalar(
#         select(FarmTask).where(
#             FarmTask.id == task_id,
#             FarmTask.farm_id == farm_id,
#         )
#     )

#     if task is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Task not found.",
#         )

#     if payload.title is not None:
#         task.title = payload.title.strip()

#     if payload.description is not None:
#         task.description = (
#             payload.description.strip()
#         )

#     if payload.date is not None:
#         task.date = payload.date

#     if payload.type is not None:
#         task.type = payload.type

#     if payload.status is not None:
#         task.status = payload.status

#     db.commit()
#     db.refresh(task)

#     return task


# @router.delete(
#     "/{farm_id}/tasks/{task_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# def delete_task(
#     farm_id: int,
#     task_id: int,
#     current_user: User = Depends(
#         get_current_user
#     ),
#     db: Session = Depends(get_db),
# ):
#     get_owned_farm(
#         farm_id,
#         current_user.id,
#         db,
#     )

#     task = db.scalar(
#         select(FarmTask).where(
#             FarmTask.id == task_id,
#             FarmTask.farm_id == farm_id,
#         )
#     )

#     if task is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Task not found.",
#         )

#     db.delete(task)
#     db.commit()

#     return None

import logging
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Farm, FarmTask, User
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.security import get_current_user

logger = logging.getLogger("krishimap.tasks")

router = APIRouter(
    prefix="/api/farms",
    tags=["Tasks"],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_owned_farm(
    farm_id: int,
    current_user: User,
    db: Session,
) -> Farm:
    """
    Return a farm only when it belongs to the authenticated user.
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


def get_owned_task(
    farm_id: int,
    task_id: int,
    current_user: User,
    db: Session,
) -> FarmTask:
    """
    Retrieve a task only when both the task and its farm belong
    to the authenticated user.
    """

    task = db.scalar(
        select(FarmTask)
        .join(Farm, Farm.id == FarmTask.farm_id)
        .where(
            FarmTask.id == task_id,
            FarmTask.farm_id == farm_id,
            Farm.owner_id == current_user.id,
        )
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


# ---------------------------------------------------------------------------
# Get tasks for a farm
# ---------------------------------------------------------------------------

@router.get(
    "/{farm_id}/tasks",
    response_model=list[TaskResponse],
)
def get_tasks(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return all tasks for an authenticated user's farm.

    Tasks are ordered by date and then ID for deterministic results.
    """

    # Verify ownership first.
    get_owned_farm(
        farm_id=farm_id,
        current_user=current_user,
        db=db,
    )

    tasks = db.scalars(
        select(FarmTask)
        .where(FarmTask.farm_id == farm_id)
        .order_by(
            FarmTask.date.asc(),
            FarmTask.id.asc(),
        )
    ).all()

    return tasks


# ---------------------------------------------------------------------------
# Create task
# ---------------------------------------------------------------------------

@router.post(
    "/{farm_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    farm_id: int,
    payload: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a task for an authenticated user's farm.
    """

    get_owned_farm(
        farm_id=farm_id,
        current_user=current_user,
        db=db,
    )

    title = payload.title.strip()

    if not title:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Task title cannot be empty",
        )

    task = FarmTask(
        farm_id=farm_id,
        title=title,
        description=(
            payload.description.strip()
            if payload.description
            else None
        ),
        date=payload.date,
        type=payload.type,
        status=payload.status,
    )

    db.add(task)

    try:
        db.commit()
        db.refresh(task)

    except IntegrityError:
        db.rollback()

        logger.exception(
            "Database integrity error while creating task "
            "for farm_id=%s",
            farm_id,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unable to create task",
        )

    except Exception:
        db.rollback()

        logger.exception(
            "Unexpected error while creating task "
            "for farm_id=%s",
            farm_id,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create task",
        )

    return task


# ---------------------------------------------------------------------------
# Update task
# ---------------------------------------------------------------------------

@router.patch(
    "/{farm_id}/tasks/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    farm_id: int,
    task_id: int,
    payload: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Partially update an existing task.
    """

    task = get_owned_task(
        farm_id=farm_id,
        task_id=task_id,
        current_user=current_user,
        db=db,
    )

    update_data = payload.model_dump(
        exclude_unset=True
    )

    if "title" in update_data:
        title = update_data["title"]

        if title is None or not title.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task title cannot be empty",
            )

        update_data["title"] = title.strip()

    if "description" in update_data:
        description = update_data["description"]

        if description is not None:
            update_data["description"] = description.strip()

    for field, value in update_data.items():
        setattr(task, field, value)

    try:
        db.commit()
        db.refresh(task)

    except Exception:
        db.rollback()

        logger.exception(
            "Unexpected error while updating task_id=%s",
            task_id,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update task",
        )

    return task


# ---------------------------------------------------------------------------
# Delete task
# ---------------------------------------------------------------------------

@router.delete(
    "/{farm_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    farm_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a task belonging to the authenticated user.
    """

    task = get_owned_task(
        farm_id=farm_id,
        task_id=task_id,
        current_user=current_user,
        db=db,
    )

    try:
        db.delete(task)
        db.commit()

    except Exception:
        db.rollback()

        logger.exception(
            "Unexpected error while deleting task_id=%s",
            task_id,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete task",
        )

    return None