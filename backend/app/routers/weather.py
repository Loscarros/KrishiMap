
# import os

# import httpx

# from dotenv import load_dotenv
# from fastapi import HTTPException


# load_dotenv()


# OPEN_METEO_URL = os.getenv(
#     "OPEN_METEO_URL",
#     "https://api.open-meteo.com/v1/forecast",
# )


# async def get_weather(
#     latitude: float,
#     longitude: float,
# ) -> dict:

#     params = {
#         "latitude": latitude,
#         "longitude": longitude,

#         "current": ",".join(
#             [
#                 "temperature_2m",
#                 "relative_humidity_2m",
#                 "precipitation",
#                 "precipitation_probability",
#                 "wind_speed_10m",
#                 "weather_code",
#             ]
#         ),

#         "daily": ",".join(
#             [
#                 "temperature_2m_max",
#                 "temperature_2m_min",
#                 "precipitation_probability_max",
#                 "rain_sum",
#                 "weather_code",
#             ]
#         ),

#         # Seven-day forecast.
#         "forecast_days": 7,

#         # Local timezone for the farm.
#         "timezone": "auto",
#     }

#     try:
#         async with httpx.AsyncClient(
#             timeout=15
#         ) as client:

#             response = await client.get(
#                 OPEN_METEO_URL,
#                 params=params,
#             )

#             response.raise_for_status()

#             data = response.json()

#             return data

#     except httpx.HTTPError as exc:

#         print(
#             "Open-Meteo error:",
#             repr(exc),
#         )

#         raise HTTPException(
#             status_code=502,
#             detail=(
#                 "Weather service is "
#                 "currently unavailable."
#             ),
#         )

import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import WeatherResponse
from app.security import get_current_user
from app.services.weather import get_weather

logger = logging.getLogger("krishimap.weather_router")

router = APIRouter(
    prefix="/api/weather",
    tags=["Weather"],
)


@router.get(
    "",
    response_model=WeatherResponse,
)
async def weather(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get weather data for the authenticated user's saved location.

    The frontend-facing endpoint and response model remain unchanged.
    """

    latitude = current_user.latitude
    longitude = current_user.longitude

    if latitude is None or longitude is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User location is not configured",
        )

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
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Weather service is temporarily unavailable",
        )

    try:
        weather_data = await get_weather(
            latitude=latitude,
            longitude=longitude,
            client=http_client,
        )

        return weather_data

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected weather error for user_id=%s",
            current_user.id,
        )

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to retrieve weather data",
        )