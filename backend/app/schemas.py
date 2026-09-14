
from datetime import date, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


# =========================================================
# AUTH
# =========================================================

class UserRegister(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=120,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    state: str = Field(
        min_length=2,
        max_length=100,
    )

    district: str = Field(
        min_length=2,
        max_length=100,
    )

    area: str = Field(
        min_length=1,
        max_length=255,
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
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


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# =========================================================
# USER LOCATION
# =========================================================

class LocationUpdate(BaseModel):
    latitude: float = Field(
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ge=-180,
        le=180,
    )


class LocationResponse(BaseModel):
    latitude: float
    longitude: float
    location_updated_at: datetime


# =========================================================
# WEATHER
# =========================================================

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
    latitude: float
    longitude: float

    current: WeatherCurrent

    daily: list[WeatherDaily]

    # Optional terrain/elevation value.
    elevation: float | None = None


# =========================================================
# CROP RECOMMENDATION
# =========================================================

class CropComparison(BaseModel):
    crop: str

    score: int = Field(
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
    # -----------------------------------------------------
    # Language
    # -----------------------------------------------------

    language: str

    # -----------------------------------------------------
    # Crop recommendation
    # -----------------------------------------------------

    intended_crop: str | None = None

    recommended_crop: str

    recommendation_score: int = Field(
        ge=0,
        le=100,
    )

    # -----------------------------------------------------
    # Backward-compatible score fields
    #
    # These are important because your existing
    # CropRecommendation.tsx displays them.
    # -----------------------------------------------------

    crop: str

    suitability_score: int = Field(
        ge=0,
        le=100,
    )

    rainfall_score: int = Field(
        ge=0,
        le=100,
    )

    temperature_score: int = Field(
        ge=0,
        le=100,
    )

    soil_score: int = Field(
        ge=0,
        le=100,
    )

    season_score: int = Field(
        ge=0,
        le=100,
    )

    vegetation_score: int = Field(
        ge=0,
        le=100,
    )

    # -----------------------------------------------------
    # AI explanation
    # -----------------------------------------------------

    why_recommended: str

    explanation: str

    # -----------------------------------------------------
    # Crop comparison
    # -----------------------------------------------------

    comparison: list[
        CropComparison
    ]

    # -----------------------------------------------------
    # Farm intelligence
    # -----------------------------------------------------

    farm_insights: list[str]

    weather_risk: list[str]

    satellite_insights: list[str]

    terrain_insights: list[str]

    # -----------------------------------------------------
    # Crop lifecycle
    # -----------------------------------------------------

    schedule: list[
        CropScheduleStage
    ]

    # -----------------------------------------------------
    # Farmer advice
    # -----------------------------------------------------

    farmer_advice: list[str]

    # -----------------------------------------------------
    # Satellite raw indicators
    # -----------------------------------------------------

    satellite_available: bool = False

    satellite: SatelliteInsights | None = None

    # -----------------------------------------------------
    # Terrain
    # -----------------------------------------------------

    topography: TopographyInsights = Field(
        default_factory=TopographyInsights
    )

    # -----------------------------------------------------
    # 7-day forecast passed through the recommendation
    # -----------------------------------------------------

    seven_day_forecast: list[
        ForecastInsight
    ] = Field(
        default_factory=list
    )


# =========================================================
# FARMS
# =========================================================

class FarmCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=120,
    )

    area_acres: float = Field(
        gt=0,
    )

    latitude: float = Field(
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ge=-180,
        le=180,
    )

    boundary: dict

    crop: str | None = Field(
        default=None,
        max_length=100,
    )


class FarmResponse(BaseModel):
    id: int

    name: str

    area_acres: float

    latitude: float

    longitude: float

    boundary: dict

    crop: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# FARM CALENDAR / TASKS
# =========================================================

class FarmTaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
    )

    description: str = Field(
        min_length=1,
        max_length=1000,
    )

    # IMPORTANT:
    # This matches SQLAlchemy Date.
    date: date

    type: str = Field(
        min_length=1,
        max_length=50,
    )

    status: str = Field(
        default="pending",
        max_length=30,
    )


class FarmTaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=1000,
    )

    # IMPORTANT:
    # Must be date, not datetime.
    date: date | None = None

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


class FarmTaskResponse(BaseModel):
    id: int

    farm_id: int

    title: str

    description: str

    date: date

    type: str

    status: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )