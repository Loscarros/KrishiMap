# from datetime import date, datetime, timezone

# from sqlalchemy import (
#     Boolean,
#     Date,
#     DateTime,
#     Float,
#     ForeignKey,
#     String,
#     Text,
# )
# from sqlalchemy.orm import (
#     Mapped,
#     mapped_column,
#     relationship,
# )

# from .database import Base


# class User(Base):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(
#         primary_key=True,
#         index=True,
#     )

#     name: Mapped[str] = mapped_column(
#         String(120),
#         nullable=False,
#     )

#     email: Mapped[str] = mapped_column(
#         String(255),
#         unique=True,
#         index=True,
#         nullable=False,
#     )

#     hashed_password: Mapped[str] = mapped_column(
#         String(255),
#         nullable=False,
#     )

#     state: Mapped[str] = mapped_column(
#         String(100),
#         nullable=False,
#     )

#     district: Mapped[str] = mapped_column(
#         String(100),
#         nullable=False,
#     )

#     area: Mapped[str] = mapped_column(
#         String(255),
#         nullable=False,
#     )

#     latitude: Mapped[float | None] = mapped_column(
#         Float,
#         nullable=True,
#     )

#     longitude: Mapped[float | None] = mapped_column(
#         Float,
#         nullable=True,
#     )

#     location_updated_at: Mapped[
#         datetime | None
#     ] = mapped_column(
#         DateTime(timezone=True),
#         nullable=True,
#     )

#     is_active: Mapped[bool] = mapped_column(
#         Boolean,
#         default=True,
#         nullable=False,
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         default=lambda: datetime.now(timezone.utc),
#         nullable=False,
#     )

#     farms: Mapped[list["Farm"]] = relationship(
#         back_populates="owner",
#         cascade="all, delete-orphan",
#     )


# class Farm(Base):
#     __tablename__ = "farms"

#     id: Mapped[int] = mapped_column(
#         primary_key=True,
#         index=True,
#     )

#     owner_id: Mapped[int] = mapped_column(
#         ForeignKey("users.id"),
#         nullable=False,
#         index=True,
#     )

#     name: Mapped[str] = mapped_column(
#         String(120),
#         nullable=False,
#     )

#     area_acres: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#     )

#     latitude: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#     )

#     longitude: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#     )

#     boundary: Mapped[str] = mapped_column(
#         Text,
#         nullable=False,
#     )

#     crop: Mapped[str | None] = mapped_column(
#         String(100),
#         nullable=True,
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         default=lambda: datetime.now(timezone.utc),
#         nullable=False,
#     )

#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         default=lambda: datetime.now(timezone.utc),
#         onupdate=lambda: datetime.now(timezone.utc),
#         nullable=False,
#     )

#     owner: Mapped["User"] = relationship(
#         back_populates="farms",
#     )

#     tasks: Mapped[list["FarmTask"]] = relationship(
#         back_populates="farm",
#         cascade="all, delete-orphan",
#     )


# class FarmTask(Base):
#     __tablename__ = "farm_tasks"

#     id: Mapped[int] = mapped_column(
#         primary_key=True,
#         index=True,
#     )

#     farm_id: Mapped[int] = mapped_column(
#         ForeignKey("farms.id"),
#         nullable=False,
#         index=True,
#     )

#     title: Mapped[str] = mapped_column(
#         String(200),
#         nullable=False,
#     )

#     description: Mapped[str] = mapped_column(
#         Text,
#         nullable=False,
#     )

#     date: Mapped[datetime] = mapped_column(
#         Date,
#         nullable=False,
#     )

#     type: Mapped[str] = mapped_column(
#         String(50),
#         nullable=False,
#     )

#     status: Mapped[str] = mapped_column(
#         String(30),
#         nullable=False,
#         default="pending",
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         default=lambda: datetime.now(timezone.utc),
#         nullable=False,
#     )

#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         default=lambda: datetime.now(timezone.utc),
#         onupdate=lambda: datetime.now(timezone.utc),
#         nullable=False,
#     )

#     farm: Mapped["Farm"] = relationship(
#         back_populates="tasks",
#     )

from datetime import date, datetime, timezone

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# ============================================================
# USER
# ============================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    district: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    area: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    location_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # --------------------------------------------------------
    # Relationships
    # --------------------------------------------------------

    farms: Mapped[list["Farm"]] = relationship(
        "Farm",
        back_populates="owner",
        cascade="all, delete-orphan",
    )


# ============================================================
# FARM
# ============================================================

class Farm(Base):
    __tablename__ = "farms"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    area_acres: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # Kept as TEXT to preserve the existing database structure.
    # GeoJSON is serialized/deserialized by the API layer.
    boundary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    crop: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # --------------------------------------------------------
    # Relationships
    # --------------------------------------------------------

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="farms",
    )

    tasks: Mapped[list["FarmTask"]] = relationship(
        "FarmTask",
        back_populates="farm",
        cascade="all, delete-orphan",
    )

    # --------------------------------------------------------
    # Indexes
    # --------------------------------------------------------
    #
    # GET /api/farms:
    #
    # WHERE owner_id = ?
    # ORDER BY created_at DESC
    #
    # This composite index makes that common query much cheaper
    # as the number of farms grows.
    # --------------------------------------------------------

    __table_args__ = (
        Index(
            "ix_farms_owner_created",
            "owner_id",
            "created_at",
        ),
    )


# ============================================================
# FARM TASK
# ============================================================

class FarmTask(Base):
    __tablename__ = "farm_tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    farm_id: Mapped[int] = mapped_column(
        ForeignKey(
            "farms.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # SQL DATE corresponds to Python datetime.date,
    # not datetime.datetime.
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # --------------------------------------------------------
    # Relationships
    # --------------------------------------------------------

    farm: Mapped["Farm"] = relationship(
        "Farm",
        back_populates="tasks",
    )

    # --------------------------------------------------------
    # Index
    # --------------------------------------------------------
    #
    # GET /api/farms/{farm_id}/tasks:
    #
    # WHERE farm_id = ?
    # ORDER BY date, id
    #
    # This avoids an expensive sort as the number of tasks grows.
    # --------------------------------------------------------

    __table_args__ = (
        Index(
            "ix_farm_tasks_farm_date_id",
            "farm_id",
            "date",
            "id",
        ),
    )