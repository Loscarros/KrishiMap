
# import json

# from fastapi import (
#     APIRouter,
#     Depends,
#     HTTPException,
#     Query,
# )

# from sqlalchemy import select
# from sqlalchemy.orm import Session

# from ..database import get_db
# from ..models import Farm, User
# from ..schemas import (
#     CropRecommendationResponse,
# )
# from ..security import (
#     get_current_user,
# )
# from ..services.recommendation import (
#     get_crop_recommendation,
# )
# from ..services.satellite import (
#     get_satellite_indicators,
# )
# from ..services.weather import (
#     get_weather,
# )


# router = APIRouter(
#     prefix="/api/recommendations",
#     tags=[
#         "AI Recommendations"
#     ],
# )


# SUPPORTED_LANGUAGES = {
#     "en",
#     "hi",
#     "bn",
# }


# @router.post(
#     "/crop/{farm_id}",
#     response_model=CropRecommendationResponse,
# )
# async def recommend_crop(
#     farm_id: int,

#     language: str = Query(
#         default="en",
#         pattern="^(en|hi|bn)$",
#     ),

#     current_user: User = Depends(
#         get_current_user
#     ),

#     db: Session = Depends(
#         get_db
#     ),
# ):
#     # =====================================================
#     # 1. Find farm owned by current farmer
#     # =====================================================

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

#     # =====================================================
#     # 2. Parse GeoJSON boundary
#     # =====================================================

#     try:
#         boundary = json.loads(
#             farm.boundary
#         )

#     except (
#         json.JSONDecodeError,
#         TypeError,
#     ) as exc:

#         print(
#             "Invalid farm boundary:",
#             exc,
#         )

#         raise HTTPException(
#             status_code=500,
#             detail=(
#                 "Farm boundary data "
#                 "is invalid."
#             ),
#         )

#     if (
#         not isinstance(
#             boundary,
#             dict,
#         )
#         or boundary.get("type")
#         != "Polygon"
#     ):
#         raise HTTPException(
#             status_code=500,
#             detail=(
#                 "Farm boundary must "
#                 "be a GeoJSON Polygon."
#             ),
#         )

#     # =====================================================
#     # 3. Get weather
#     #
#     # Includes:
#     # - current weather
#     # - 7-day forecast
#     # - elevation
#     # =====================================================

#     weather = await get_weather(
#         farm.latitude,
#         farm.longitude,
#     )

#     current_weather = weather.get(
#         "current",
#         {},
#     )

#     daily_weather = weather.get(
#         "daily",
#         {},
#     )

#     elevation = weather.get(
#         "elevation"
#     )

#     # =====================================================
#     # 4. Build seven-day forecast
#     # =====================================================

#     dates = daily_weather.get(
#         "time",
#         [],
#     )

#     temperature_max = (
#         daily_weather.get(
#             "temperature_2m_max",
#             [],
#         )
#     )

#     temperature_min = (
#         daily_weather.get(
#             "temperature_2m_min",
#             [],
#         )
#     )

#     rainfall = (
#         daily_weather.get(
#             "rain_sum",
#             [],
#         )
#     )

#     precipitation_probability = (
#         daily_weather.get(
#             "precipitation_probability_max",
#             [],
#         )
#     )

#     weather_codes = (
#         daily_weather.get(
#             "weather_code",
#             [],
#         )
#     )

#     forecast = []

#     for index, forecast_date in enumerate(
#         dates[:7]
#     ):
#         forecast.append(
#             {
#                 "date": forecast_date,

#                 "temperature_max": (
#                     temperature_max[index]
#                     if index < len(
#                         temperature_max
#                     )
#                     else None
#                 ),

#                 "temperature_min": (
#                     temperature_min[index]
#                     if index < len(
#                         temperature_min
#                     )
#                     else None
#                 ),

#                 "rainfall": (
#                     rainfall[index]
#                     if index < len(
#                         rainfall
#                     )
#                     else None
#                 ),

#                 "precipitation_probability": (
#                     precipitation_probability[index]
#                     if index < len(
#                         precipitation_probability
#                     )
#                     else None
#                 ),

#                 "weather_code": (
#                     weather_codes[index]
#                     if index < len(
#                         weather_codes
#                     )
#                     else None
#                 ),
#             }
#         )

#     # =====================================================
#     # 5. Get Sentinel-2 indicators
#     #
#     # If Sentinel credentials are missing
#     # or the service fails, this returns:
#     #
#     # available = False
#     #
#     # The recommendation still works.
#     # =====================================================

#     satellite = (
#         await get_satellite_indicators(
#             boundary
#         )
#     )

#     # =====================================================
#     # 6. Build terrain context
#     # =====================================================

#     terrain = {
#         "elevation_meters": elevation,

#         "source": (
#             "Open-Meteo elevation data"
#         ),

#         "interpretation": (
#             "Elevation is a terrain "
#             "indicator and is not a "
#             "complete topographic survey."
#         ),
#     }

#     # =====================================================
#     # 7. Build farm intelligence context
#     # =====================================================

#     farm_context = {
#         "language": language,

#         "farmer": {
#             "state":
#                 current_user.state,

#             "district":
#                 current_user.district,
#         },

#         "farm": {
#             "name":
#                 farm.name,

#             "area_acres":
#                 farm.area_acres,

#             "latitude":
#                 farm.latitude,

#             "longitude":
#                 farm.longitude,

#             "current_crop":
#                 farm.crop,

#             "boundary":
#                 boundary,
#         },

#         "terrain":
#             terrain,

#         "weather": {
#             "current": {
#                 "temperature":
#                     current_weather.get(
#                         "temperature_2m"
#                     ),

#                 "humidity":
#                     current_weather.get(
#                         "relative_humidity_2m"
#                     ),

#                 "rainfall":
#                     current_weather.get(
#                         "precipitation"
#                     ),

#                 "precipitation_probability":
#                     current_weather.get(
#                         "precipitation_probability"
#                     ),

#                 "wind_speed":
#                     current_weather.get(
#                         "wind_speed_10m"
#                     ),

#                 "weather_code":
#                     current_weather.get(
#                         "weather_code"
#                     ),
#             },

#             "seven_day_forecast":
#                 forecast,
#         },

#         "satellite":
#             satellite,
#     }

#     # =====================================================
#     # 8. Ask deterministic backend + Groq
#     # =====================================================

#     try:
#         recommendation = (
#             get_crop_recommendation(
#                 farm_context=farm_context,
#                 language=language,
#             )
#         )

#     except Exception as exc:
#         print(
#             "AI recommendation error:",
#             repr(exc),
#         )

#         raise HTTPException(
#             status_code=502,
#             detail=(
#                 "AI recommendation "
#                 "service is currently "
#                 "unavailable."
#             ),
#         )

#     # =====================================================
#     # 9. Add raw satellite/topography/forecast
#     #
#     # These are backend facts, not LLM-generated facts.
#     # =====================================================

#     recommendation[
#         "satellite_available"
#     ] = bool(
#         satellite.get(
#             "available",
#             False,
#         )
#     )

#     recommendation[
#         "satellite"
#     ] = satellite

#     recommendation[
#         "topography"
#     ] = {
#         "elevation_m":
#             elevation,

#         "source":
#             terrain["source"],

#         "interpretation":
#             terrain["interpretation"],
#     }

#     recommendation[
#         "seven_day_forecast"
#     ] = forecast

#     # Ensure language cannot be changed
#     # by the LLM.
#     recommendation[
#         "language"
#     ] = language

#     return recommendation

import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Farm, User
from app.schemas import CropRecommendationResponse
from app.security import get_current_user
from app.services.recommendation import get_crop_recommendation
from app.services.satellite import get_satellite_indicators
from app.services.weather import get_weather


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"],
)


logger = logging.getLogger("krishimap.recommendations")


# ============================================================
# SUPPORTED LANGUAGES
# ============================================================

SUPPORTED_LANGUAGES = {
    "en",
    "hi",
    "bn",
}


# ============================================================
# CROP RECOMMENDATION
# ============================================================

@router.post(
    "/crop/{farm_id}",
    response_model=CropRecommendationResponse,
)
async def crop_recommendation(
    farm_id: int,
    request: Request,
    language: str = Query(
        default="en",
        pattern="^(en|hi|bn)$",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate an AI-assisted crop recommendation for a farm.

    Frontend contract:
        POST /api/recommendations/crop/{farm_id}?language=en|hi|bn

    The request and response structures are intentionally kept
    compatible with the existing frontend.
    """

    # ========================================================
    # LANGUAGE VALIDATION
    # ========================================================

    language = language.lower().strip()

    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported language.",
        )

    # ========================================================
    # FETCH FARM
    # ========================================================

    result = db.execute(
        select(Farm).where(
            Farm.id == farm_id,
            Farm.owner_id == current_user.id,
        )
    )

    farm = result.scalar_one_or_none()

    if farm is None:
        raise HTTPException(
            status_code=404,
            detail="Farm not found.",
        )

    # ========================================================
    # PARSE FARM BOUNDARY
    # ========================================================

    try:
        boundary = json.loads(farm.boundary)

    except (TypeError, json.JSONDecodeError):
        logger.error(
            "Invalid boundary JSON for farm_id=%s",
            farm_id,
        )

        raise HTTPException(
            status_code=500,
            detail="Farm boundary data is invalid.",
        )

    # ========================================================
    # VALIDATE GEOJSON TYPE
    # ========================================================

    if not isinstance(boundary, dict):
        raise HTTPException(
            status_code=422,
            detail="Farm boundary must be a GeoJSON object.",
        )

    if boundary.get("type") != "Polygon":
        raise HTTPException(
            status_code=422,
            detail="Farm boundary must be a GeoJSON Polygon.",
        )

    # ========================================================
    # SHARED HTTP CLIENT
    # ========================================================

    http_client = getattr(
        request.app.state,
        "http_client",
        None,
    )

    if http_client is None:
        logger.error(
            "Shared HTTP client is not initialized."
        )

        raise HTTPException(
            status_code=503,
            detail="External service client is unavailable.",
        )

    # ========================================================
    # WEATHER
    # ========================================================

    try:
        weather = await get_weather(
            farm.latitude,
            farm.longitude,
            http_client,
        )

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected weather error for farm_id=%s",
            farm_id,
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve weather information.",
        )

    # ========================================================
    # EXTRACT WEATHER DATA
    # ========================================================

    current_weather = weather.get(
        "current",
        {},
    )

    daily_weather = weather.get(
        "daily",
        {},
    )

    elevation = weather.get(
        "elevation",
    )

    # ========================================================
    # SATELLITE DATA
    # ========================================================

    try:
        satellite = await get_satellite_indicators(
            boundary
        )

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Satellite service failed for farm_id=%s",
            farm_id,
        )

        # Satellite data is an optional enrichment.
        #
        # The recommendation engine already knows how to handle
        # unavailable satellite indicators, so don't make the
        # entire recommendation unavailable because satellite
        # data failed.
        satellite = {
            "available": False,
            "source": None,
            "acquisition_window_days": None,
            "ndvi": None,
            "ndmi": None,
            "bsi": None,
            "cloud_masked": False,
        }

    # ========================================================
    # BUILD FARM CONTEXT
    # ========================================================

    farm_context = {
        "language": language,

        "farmer": {
            "state": current_user.state,
            "district": current_user.district,
            "area": current_user.area,
        },

        "farm": {
            "id": farm.id,
            "name": farm.name,
            "area_acres": farm.area_acres,
            "latitude": farm.latitude,
            "longitude": farm.longitude,
            "current_crop": farm.crop,
            "boundary": boundary,
        },

        "terrain": {
            "elevation": elevation,
        },

        "weather": {
            "current": current_weather,
            "daily": daily_weather,
        },

        "satellite": satellite,
    }

    # ========================================================
    # AI RECOMMENDATION
    # ========================================================
    #
    # IMPORTANT:
    #
    # get_crop_recommendation() is synchronous because the
    # LangChain/Groq call currently uses chain.invoke().
    #
    # Calling it directly inside an async FastAPI endpoint would
    # block the event loop.
    #
    # run_in_threadpool() moves the blocking operation away from
    # the event loop, allowing other requests to continue.
    # ========================================================

    try:
        recommendation = await run_in_threadpool(
            get_crop_recommendation,
            farm_context,
            language,
        )

    except Exception:
        logger.exception(
            "Crop recommendation failed for farm_id=%s",
            farm_id,
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to generate crop recommendation.",
        )

    # ========================================================
    # ADD RAW DATA TO RESPONSE
    # ========================================================
    #
    # These fields are preserved because your existing frontend
    # expects the recommendation response to contain these
    # contextual values.
    # ========================================================

    recommendation["satellite"] = satellite

    recommendation["terrain"] = {
        "elevation": elevation,
    }

    recommendation["forecast"] = daily_weather

    recommendation["language"] = language

    # ========================================================
    # RESPONSE
    # ========================================================

    return recommendation