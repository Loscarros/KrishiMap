
# from datetime import date, datetime

# from pydantic import (
#     BaseModel,
#     ConfigDict,
#     EmailStr,
#     Field,
# )


# # =========================================================
# # AUTH
# # =========================================================

# class UserRegister(BaseModel):
#     name: str = Field(
#         min_length=2,
#         max_length=120,
#     )

#     email: EmailStr

#     password: str = Field(
#         min_length=8,
#         max_length=128,
#     )

#     state: str = Field(
#         min_length=2,
#         max_length=100,
#     )

#     district: str = Field(
#         min_length=2,
#         max_length=100,
#     )

#     area: str = Field(
#         min_length=1,
#         max_length=255,
#     )


# class UserResponse(BaseModel):
#     model_config = ConfigDict(
#         from_attributes=True
#     )

#     id: int
#     name: str
#     email: EmailStr
#     state: str
#     district: str
#     area: str

#     latitude: float | None = None
#     longitude: float | None = None

#     location_updated_at: datetime | None = None


# class TokenResponse(BaseModel):
#     access_token: str
#     token_type: str


# # =========================================================
# # USER LOCATION
# # =========================================================

# class LocationUpdate(BaseModel):
#     latitude: float = Field(
#         ge=-90,
#         le=90,
#     )

#     longitude: float = Field(
#         ge=-180,
#         le=180,
#     )


# class LocationResponse(BaseModel):
#     latitude: float
#     longitude: float
#     location_updated_at: datetime


# # =========================================================
# # WEATHER
# # =========================================================

# class WeatherCurrent(BaseModel):
#     temperature: float | None = None
#     humidity: float | None = None
#     rainfall: float | None = None
#     precipitation_probability: float | None = None
#     wind_speed: float | None = None
#     weather_code: int | None = None


# class WeatherDaily(BaseModel):
#     date: str

#     temperature_max: float | None = None

#     temperature_min: float | None = None

#     precipitation_probability: float | None = None

#     rainfall: float | None = None

#     weather_code: int | None = None


# class WeatherResponse(BaseModel):
#     latitude: float
#     longitude: float

#     current: WeatherCurrent

#     daily: list[WeatherDaily]

#     # Optional terrain/elevation value.
#     elevation: float | None = None


# # =========================================================
# # CROP RECOMMENDATION
# # =========================================================

# class CropComparison(BaseModel):
#     crop: str

#     score: int = Field(
#         ge=0,
#         le=100,
#     )

#     reason: str


# class CropScheduleStage(BaseModel):
#     stage: str

#     start_day: int = Field(
#         ge=0,
#     )

#     end_day: int = Field(
#         ge=0,
#     )

#     activities: list[str]


# class SatelliteInsights(BaseModel):
#     available: bool = False

#     source: str | None = None

#     acquisition_window_days: int | None = None

#     ndvi: float | None = None

#     ndmi: float | None = None

#     bsi: float | None = None

#     cloud_masked: bool = True


# class TopographyInsights(BaseModel):
#     elevation_m: float | None = None

#     source: str | None = None

#     interpretation: str | None = None


# class ForecastInsight(BaseModel):
#     date: str

#     temperature_max: float | None = None

#     temperature_min: float | None = None

#     rainfall: float | None = None

#     precipitation_probability: float | None = None

#     weather_code: int | None = None


# class CropRecommendationResponse(BaseModel):
#     # -----------------------------------------------------
#     # Language
#     # -----------------------------------------------------

#     language: str

#     # -----------------------------------------------------
#     # Crop recommendation
#     # -----------------------------------------------------

#     intended_crop: str | None = None

#     recommended_crop: str

#     recommendation_score: int = Field(
#         ge=0,
#         le=100,
#     )

#     # -----------------------------------------------------
#     # Backward-compatible score fields
#     #
#     # These are important because your existing
#     # CropRecommendation.tsx displays them.
#     # -----------------------------------------------------

#     crop: str

#     suitability_score: int = Field(
#         ge=0,
#         le=100,
#     )

#     rainfall_score: int = Field(
#         ge=0,
#         le=100,
#     )

#     temperature_score: int = Field(
#         ge=0,
#         le=100,
#     )

#     soil_score: int = Field(
#         ge=0,
#         le=100,
#     )

#     season_score: int = Field(
#         ge=0,
#         le=100,
#     )

#     vegetation_score: int = Field(
#         ge=0,
#         le=100,
#     )

#     # -----------------------------------------------------
#     # AI explanation
#     # -----------------------------------------------------

#     why_recommended: str

#     explanation: str

#     # -----------------------------------------------------
#     # Crop comparison
#     # -----------------------------------------------------

#     comparison: list[
#         CropComparison
#     ]

#     # -----------------------------------------------------
#     # Farm intelligence
#     # -----------------------------------------------------

#     farm_insights: list[str]

#     weather_risk: list[str]

#     satellite_insights: list[str]

#     terrain_insights: list[str]

#     # -----------------------------------------------------
#     # Crop lifecycle
#     # -----------------------------------------------------

#     schedule: list[
#         CropScheduleStage
#     ]

#     # -----------------------------------------------------
#     # Farmer advice
#     # -----------------------------------------------------

#     farmer_advice: list[str]

#     # -----------------------------------------------------
#     # Satellite raw indicators
#     # -----------------------------------------------------

#     satellite_available: bool = False

#     satellite: SatelliteInsights | None = None

#     # -----------------------------------------------------
#     # Terrain
#     # -----------------------------------------------------

#     topography: TopographyInsights = Field(
#         default_factory=TopographyInsights
#     )

#     # -----------------------------------------------------
#     # 7-day forecast passed through the recommendation
#     # -----------------------------------------------------

#     seven_day_forecast: list[
#         ForecastInsight
#     ] = Field(
#         default_factory=list
#     )


# # =========================================================
# # FARMS
# # =========================================================

# class FarmCreate(BaseModel):
#     name: str = Field(
#         min_length=1,
#         max_length=120,
#     )

#     area_acres: float = Field(
#         gt=0,
#     )

#     latitude: float = Field(
#         ge=-90,
#         le=90,
#     )

#     longitude: float = Field(
#         ge=-180,
#         le=180,
#     )

#     boundary: dict

#     crop: str | None = Field(
#         default=None,
#         max_length=100,
#     )


# class FarmResponse(BaseModel):
#     id: int

#     name: str

#     area_acres: float

#     latitude: float

#     longitude: float

#     boundary: dict

#     crop: str | None = None

#     model_config = ConfigDict(
#         from_attributes=True
#     )


# # =========================================================
# # FARM CALENDAR / TASKS
# # =========================================================

# class FarmTaskCreate(BaseModel):
#     title: str = Field(
#         min_length=1,
#         max_length=200,
#     )

#     description: str = Field(
#         min_length=1,
#         max_length=1000,
#     )

#     # IMPORTANT:
#     # This matches SQLAlchemy Date.
#     date: date

#     type: str = Field(
#         min_length=1,
#         max_length=50,
#     )

#     status: str = Field(
#         default="pending",
#         max_length=30,
#     )


# class FarmTaskUpdate(BaseModel):
#     title: str | None = Field(
#         default=None,
#         min_length=1,
#         max_length=200,
#     )

#     description: str | None = Field(
#         default=None,
#         min_length=1,
#         max_length=1000,
#     )

#     # IMPORTANT:
#     # Must be date, not datetime.
#     date: date | None = None

#     type: str | None = Field(
#         default=None,
#         min_length=1,
#         max_length=50,
#     )

#     status: str | None = Field(
#         default=None,
#         min_length=1,
#         max_length=30,
#     )


# class FarmTaskResponse(BaseModel):
#     id: int

#     farm_id: int

#     title: str

#     description: str

#     date: date

#     type: str

#     status: str

#     created_at: datetime

#     updated_at: datetime

#     model_config = ConfigDict(
#         from_attributes=True
#     )

from datetime import date, datetime
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


# ============================================================================
# USER SCHEMAS
# ============================================================================

class UserCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=120,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    state: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    district: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    area: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90,
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180,
    )

    @field_validator("name", "state", "district", "area")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty.")

        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    name: str
    email: EmailStr
    state: str
    district: str
    area: str

    latitude: float | None = None
    longitude: float | None = None

    location_updated_at: datetime | None = None

    is_active: bool
    created_at: datetime


# ============================================================================
# AUTHENTICATION SCHEMAS
# ============================================================================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# ============================================================================
# USER LOCATION
# ============================================================================

class LocationUpdate(BaseModel):
    latitude: float = Field(
        ...,
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180,
    )


class LocationResponse(BaseModel):
    latitude: float
    longitude: float
    location_updated_at: datetime


# ============================================================================
# WEATHER SCHEMAS
# ============================================================================

class WeatherCurrent(BaseModel):
    temperature: float | None = None
    humidity: float | None = None
    rainfall: float | None = None
    precipitation_probability: float | None = None
    wind_speed: float | None = None
    weather_code: int | None = None


class WeatherDaily(BaseModel):
    date: str

    temperature_max: float | None = None
    temperature_min: float | None = None

    precipitation_probability: float | None = None

    rainfall: float | None = None

    weather_code: int | None = None


class WeatherResponse(BaseModel):
    """
    Open-Meteo response.

    Extra fields are allowed because Open-Meteo can return additional
    metadata without requiring a backend deployment.
    """

    model_config = ConfigDict(
        extra="allow",
    )

    latitude: float | None = None
    longitude: float | None = None

    elevation: float | None = None

    timezone: str | None = None
    timezone_abbreviation: str | None = None
    utc_offset_seconds: int | None = None

    current: dict[str, Any]
    daily: dict[str, Any]

    current_units: dict[str, Any] | None = None
    daily_units: dict[str, Any] | None = None


# ============================================================================
# CROP RECOMMENDATION SCHEMAS
# ============================================================================

class CropRecommendationRequest(BaseModel):
    language: Literal["en", "hi", "bn"] = "en"


class CropComparison(BaseModel):
    crop: str

    score: float = Field(
        ge=0,
        le=100,
    )

    reason: str


class CropScheduleStage(BaseModel):
    stage: str

    start_day: int = Field(
        ge=0,
    )

    end_day: int = Field(
        ge=0,
    )

    activities: list[str]


class SatelliteInsights(BaseModel):
    available: bool = False

    source: str | None = None

    acquisition_window_days: int | None = None

    ndvi: float | None = None

    ndmi: float | None = None

    bsi: float | None = None

    cloud_masked: bool = True


class TopographyInsights(BaseModel):
    elevation_m: float | None = None

    source: str | None = None

    interpretation: str | None = None


class ForecastInsight(BaseModel):
    date: str

    temperature_max: float | None = None
    temperature_min: float | None = None

    rainfall: float | None = None

    precipitation_probability: float | None = None

    weather_code: int | None = None


class CropRecommendationResponse(BaseModel):
    """
    Recommendation response.

    The stable frontend fields are explicitly defined while extra
    metadata from the AI, satellite, terrain, or forecast services
    is allowed for forward compatibility.
    """

    model_config = ConfigDict(
        extra="allow",
    )

    # ------------------------------------------------------------------------
    # Language
    # ------------------------------------------------------------------------

    language: str

    # ------------------------------------------------------------------------
    # Crop recommendation
    # ------------------------------------------------------------------------

    intended_crop: str | None = None

    recommended_crop: str

    recommendation_score: float = Field(
        ge=0,
        le=100,
    )

    # ------------------------------------------------------------------------
    # AI explanation
    # ------------------------------------------------------------------------

    why_recommended: str

    explanation: str | None = None

    # ------------------------------------------------------------------------
    # Crop comparison
    # ------------------------------------------------------------------------

    comparison: list[dict[str, Any]] = Field(
        default_factory=list,
    )

    # ------------------------------------------------------------------------
    # Farm intelligence
    # ------------------------------------------------------------------------

    farm_insights: list[str] = Field(
        default_factory=list,
    )

    weather_risk: list[str] = Field(
        default_factory=list,
    )

    satellite_insights: list[str] = Field(
        default_factory=list,
    )

    terrain_insights: list[str] = Field(
        default_factory=list,
    )

    # ------------------------------------------------------------------------
    # Crop lifecycle
    # ------------------------------------------------------------------------

    schedule: list[dict[str, Any]] = Field(
        default_factory=list,
    )

    # ------------------------------------------------------------------------
    # Farmer advice
    # ------------------------------------------------------------------------

    farmer_advice: list[str] = Field(
        default_factory=list,
    )

    # ------------------------------------------------------------------------
    # Backward-compatible score fields
    # ------------------------------------------------------------------------

    crop: str | None = None

    suitability_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    rainfall_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    temperature_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    soil_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    season_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    vegetation_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    # ------------------------------------------------------------------------
    # Satellite / terrain / forecast
    # ------------------------------------------------------------------------

    satellite_available: bool = False

    satellite: SatelliteInsights | dict[str, Any] | None = None

    topography: TopographyInsights = Field(
        default_factory=TopographyInsights,
    )

    terrain: dict[str, Any] | None = None

    seven_day_forecast: list[ForecastInsight] = Field(
        default_factory=list,
    )

    forecast: dict[str, Any] | None = None


# ============================================================================
# FARM SCHEMAS
# ============================================================================

class FarmCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )

    area_acres: float = Field(
        ...,
        gt=0,
    )

    latitude: float = Field(
        ...,
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180,
    )

    boundary: dict[str, Any] | list[Any]

    crop: str | None = Field(
        default=None,
        max_length=100,
    )

    @field_validator("name", "crop")
    @classmethod
    def strip_strings(cls, value: str | None):
        if value is None:
            return None

        value = value.strip()

        return value or None


class FarmResponse(BaseModel):
    """
    Preserve the existing frontend farm response contract.

    Database timestamps remain available internally but are not exposed
    here because they were not part of the original frontend response.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    name: str
    area_acres: float
    latitude: float
    longitude: float
    boundary: dict[str, Any] | list[Any]
    crop: str | None = None


# ============================================================================
# FARM CALENDAR / TASK SCHEMAS
# ============================================================================

class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
    )

    description: str = Field(
        default="",
        max_length=1000,
    )

    date: date

    type: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    status: str = Field(
        default="pending",
        min_length=1,
        max_length=30,
    )

    @field_validator("title", "description", "type", "status")
    @classmethod
    def strip_strings(cls, value: str):
        value = value.strip()

        return value


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    date: datetime | None = None

    type: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    status: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    @field_validator("title", "description", "type", "status")
    @classmethod
    def strip_optional_strings(cls, value: str | None):
        if value is None:
            return None

        return value.strip()


class TaskResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    farm_id: int
    title: str
    description: str
    date: date
    type: str
    status: str
    created_at: datetime
    updated_at: datetime


# ============================================================================
# BACKWARD-COMPATIBILITY ALIASES
# ============================================================================
#
# These aliases allow older router/import code to continue working if
# any part of the backend still uses the original schema names.
# ============================================================================

UserRegister = UserCreate

FarmTaskCreate = TaskCreate
FarmTaskUpdate = TaskUpdate
FarmTaskResponse = TaskResponse