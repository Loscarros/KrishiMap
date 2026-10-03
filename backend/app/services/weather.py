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
# ):
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

#         # Open-Meteo can return the
#         # elevation used by its terrain
#         # downscaling.
#         "elevation": "90",

#         "forecast_days": 7,

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

#             return response.json()

#     except httpx.HTTPError as exc:
#         print(
#             "Open-Meteo error:",
#             exc,
#         )

#         raise HTTPException(
#             status_code=502,
#             detail=(
#                 "Weather service is "
#                 "currently unavailable."
#             ),
#         )

import asyncio
import logging
from typing import Any

import httpx
from fastapi import HTTPException

logger = logging.getLogger("krishimap.weather")


# ============================================================
# CONFIGURATION
# ============================================================

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Number of attempts for temporary upstream failures.
MAX_RETRIES = 2

# Small delay between retry attempts.
RETRY_DELAY_SECONDS = 0.5


# ============================================================
# WEATHER SERVICE
# ============================================================

async def get_weather(
    latitude: float,
    longitude: float,
    client: httpx.AsyncClient,
) -> dict[str, Any]:
    """
    Fetch current weather and a 7-day forecast from Open-Meteo.

    IMPORTANT:
    The returned structure is intentionally kept compatible with
    the existing KrishiMap frontend/recommendation service.

    Parameters
    ----------
    latitude:
        Farm latitude.

    longitude:
        Farm longitude.

    client:
        Shared application-level httpx.AsyncClient.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,

        # Current weather
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "precipitation_probability,"
            "wind_speed_10m,"
            "weather_code"
        ),

        # Seven-day forecast
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "rain_sum,"
            "weather_code"
        ),

        "forecast_days": 7,

        # Let Open-Meteo return the correct local timezone.
        "timezone": "auto",
    }

    last_exception: Exception | None = None

    # ========================================================
    # REQUEST WITH LIMITED RETRIES
    # ========================================================

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = await client.get(
                OPEN_METEO_URL,
                params=params,
            )

            # Convert 4xx/5xx responses into exceptions.
            response.raise_for_status()

            data = response.json()

            # Basic upstream response validation.
            if not isinstance(data, dict):
                raise ValueError(
                    "Open-Meteo returned an invalid response."
                )

            if "current" not in data:
                raise ValueError(
                    "Open-Meteo response is missing current weather data."
                )

            if "daily" not in data:
                raise ValueError(
                    "Open-Meteo response is missing daily forecast data."
                )

            return data

        except (
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.RemoteProtocolError,
        ) as exc:
            last_exception = exc

            logger.warning(
                "Open-Meteo request failed "
                "(attempt %s/%s): %s",
                attempt + 1,
                MAX_RETRIES + 1,
                exc,
            )

            # Don't retry after the final attempt.
            if attempt >= MAX_RETRIES:
                break

            await asyncio.sleep(
                RETRY_DELAY_SECONDS * (attempt + 1)
            )

        except httpx.HTTPStatusError as exc:
            last_exception = exc

            status_code = exc.response.status_code

            logger.warning(
                "Open-Meteo returned HTTP %s "
                "(attempt %s/%s).",
                status_code,
                attempt + 1,
                MAX_RETRIES + 1,
            )

            # Retry only temporary upstream/server failures.
            #
            # 4xx errors generally indicate a bad request and
            # should not be repeatedly retried.
            if status_code < 500 or attempt >= MAX_RETRIES:
                break

            await asyncio.sleep(
                RETRY_DELAY_SECONDS * (attempt + 1)
            )

        except ValueError as exc:
            # Invalid JSON / malformed upstream response.
            last_exception = exc

            logger.exception(
                "Open-Meteo returned an invalid response."
            )

            break

        except Exception as exc:
            # Unexpected errors should not expose internal details
            # to the frontend.
            last_exception = exc

            logger.exception(
                "Unexpected error while requesting weather data."
            )

            break

    # ========================================================
    # SAFE API ERROR
    # ========================================================

    logger.error(
        "Unable to retrieve weather data from Open-Meteo: %s",
        last_exception,
    )

    raise HTTPException(
        status_code=502,
        detail="Weather service is temporarily unavailable.",
    )