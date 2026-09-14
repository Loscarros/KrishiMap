
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
) -> dict:

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

        # Seven-day forecast.
        "forecast_days": 7,

        # Local timezone for the farm.
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

            data = response.json()

            return data

    except httpx.HTTPError as exc:

        print(
            "Open-Meteo error:",
            repr(exc),
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "Weather service is "
                "currently unavailable."
            ),
        )