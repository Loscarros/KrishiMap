
import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Farm, User
from ..schemas import (
    CropRecommendationResponse,
)
from ..security import (
    get_current_user,
)
from ..services.recommendation import (
    get_crop_recommendation,
)
from ..services.satellite import (
    get_satellite_indicators,
)
from ..services.weather import (
    get_weather,
)


router = APIRouter(
    prefix="/api/recommendations",
    tags=[
        "AI Recommendations"
    ],
)


SUPPORTED_LANGUAGES = {
    "en",
    "hi",
    "bn",
}


@router.post(
    "/crop/{farm_id}",
    response_model=CropRecommendationResponse,
)
async def recommend_crop(
    farm_id: int,

    language: str = Query(
        default="en",
        pattern="^(en|hi|bn)$",
    ),

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    ),
):
    # =====================================================
    # 1. Find farm owned by current farmer
    # =====================================================

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

    # =====================================================
    # 2. Parse GeoJSON boundary
    # =====================================================

    try:
        boundary = json.loads(
            farm.boundary
        )

    except (
        json.JSONDecodeError,
        TypeError,
    ) as exc:

        print(
            "Invalid farm boundary:",
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Farm boundary data "
                "is invalid."
            ),
        )

    if (
        not isinstance(
            boundary,
            dict,
        )
        or boundary.get("type")
        != "Polygon"
    ):
        raise HTTPException(
            status_code=500,
            detail=(
                "Farm boundary must "
                "be a GeoJSON Polygon."
            ),
        )

    # =====================================================
    # 3. Get weather
    #
    # Includes:
    # - current weather
    # - 7-day forecast
    # - elevation
    # =====================================================

    weather = await get_weather(
        farm.latitude,
        farm.longitude,
    )

    current_weather = weather.get(
        "current",
        {},
    )

    daily_weather = weather.get(
        "daily",
        {},
    )

    elevation = weather.get(
        "elevation"
    )

    # =====================================================
    # 4. Build seven-day forecast
    # =====================================================

    dates = daily_weather.get(
        "time",
        [],
    )

    temperature_max = (
        daily_weather.get(
            "temperature_2m_max",
            [],
        )
    )

    temperature_min = (
        daily_weather.get(
            "temperature_2m_min",
            [],
        )
    )

    rainfall = (
        daily_weather.get(
            "rain_sum",
            [],
        )
    )

    precipitation_probability = (
        daily_weather.get(
            "precipitation_probability_max",
            [],
        )
    )

    weather_codes = (
        daily_weather.get(
            "weather_code",
            [],
        )
    )

    forecast = []

    for index, forecast_date in enumerate(
        dates[:7]
    ):
        forecast.append(
            {
                "date": forecast_date,

                "temperature_max": (
                    temperature_max[index]
                    if index < len(
                        temperature_max
                    )
                    else None
                ),

                "temperature_min": (
                    temperature_min[index]
                    if index < len(
                        temperature_min
                    )
                    else None
                ),

                "rainfall": (
                    rainfall[index]
                    if index < len(
                        rainfall
                    )
                    else None
                ),

                "precipitation_probability": (
                    precipitation_probability[index]
                    if index < len(
                        precipitation_probability
                    )
                    else None
                ),

                "weather_code": (
                    weather_codes[index]
                    if index < len(
                        weather_codes
                    )
                    else None
                ),
            }
        )

    # =====================================================
    # 5. Get Sentinel-2 indicators
    #
    # If Sentinel credentials are missing
    # or the service fails, this returns:
    #
    # available = False
    #
    # The recommendation still works.
    # =====================================================

    satellite = (
        await get_satellite_indicators(
            boundary
        )
    )

    # =====================================================
    # 6. Build terrain context
    # =====================================================

    terrain = {
        "elevation_meters": elevation,

        "source": (
            "Open-Meteo elevation data"
        ),

        "interpretation": (
            "Elevation is a terrain "
            "indicator and is not a "
            "complete topographic survey."
        ),
    }

    # =====================================================
    # 7. Build farm intelligence context
    # =====================================================

    farm_context = {
        "language": language,

        "farmer": {
            "state":
                current_user.state,

            "district":
                current_user.district,
        },

        "farm": {
            "name":
                farm.name,

            "area_acres":
                farm.area_acres,

            "latitude":
                farm.latitude,

            "longitude":
                farm.longitude,

            "current_crop":
                farm.crop,

            "boundary":
                boundary,
        },

        "terrain":
            terrain,

        "weather": {
            "current": {
                "temperature":
                    current_weather.get(
                        "temperature_2m"
                    ),

                "humidity":
                    current_weather.get(
                        "relative_humidity_2m"
                    ),

                "rainfall":
                    current_weather.get(
                        "precipitation"
                    ),

                "precipitation_probability":
                    current_weather.get(
                        "precipitation_probability"
                    ),

                "wind_speed":
                    current_weather.get(
                        "wind_speed_10m"
                    ),

                "weather_code":
                    current_weather.get(
                        "weather_code"
                    ),
            },

            "seven_day_forecast":
                forecast,
        },

        "satellite":
            satellite,
    }

    # =====================================================
    # 8. Ask deterministic backend + Groq
    # =====================================================

    try:
        recommendation = (
            get_crop_recommendation(
                farm_context=farm_context,
                language=language,
            )
        )

    except Exception as exc:
        print(
            "AI recommendation error:",
            repr(exc),
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "AI recommendation "
                "service is currently "
                "unavailable."
            ),
        )

    # =====================================================
    # 9. Add raw satellite/topography/forecast
    #
    # These are backend facts, not LLM-generated facts.
    # =====================================================

    recommendation[
        "satellite_available"
    ] = bool(
        satellite.get(
            "available",
            False,
        )
    )

    recommendation[
        "satellite"
    ] = satellite

    recommendation[
        "topography"
    ] = {
        "elevation_m":
            elevation,

        "source":
            terrain["source"],

        "interpretation":
            terrain["interpretation"],
    }

    recommendation[
        "seven_day_forecast"
    ] = forecast

    # Ensure language cannot be changed
    # by the LLM.
    recommendation[
        "language"
    ] = language

    return recommendation