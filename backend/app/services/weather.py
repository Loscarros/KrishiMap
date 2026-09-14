import os

import httpx

from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()


OPEN_METEO_URL = os.getenv(
    "OPEN_METEO_URL",
    "https://api.open-meteo.com/v1/forecast",
)


async def get_weather(
    latitude: float,
    longitude: float,
):
    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": ",".join(
            [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "precipitation_probability",
                "wind_speed_10m",
                "weather_code",
            ]
        ),

        "daily": ",".join(
            [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
                "rain_sum",
                "weather_code",
            ]
        ),

        # Open-Meteo can return the
        # elevation used by its terrain
        # downscaling.
        "elevation": "90",

        "forecast_days": 7,

        "timezone": "auto",
    }

    try:
        async with httpx.AsyncClient(
            timeout=15
        ) as client:

            response = await client.get(
                OPEN_METEO_URL,
                params=params,
            )

            response.raise_for_status()

            return response.json()

    except httpx.HTTPError as exc:
        print(
            "Open-Meteo error:",
            exc,
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "Weather service is "
                "currently unavailable."
            ),
        )