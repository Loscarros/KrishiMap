
import json
import os
from typing import Any

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


load_dotenv()


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)


if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not configured"
    )


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0.1,
)


# =========================================================
# CROP KNOWLEDGE
# =========================================================

CROP_PROFILES: dict[str, dict[str, Any]] = {
    "Rice": {
        "temperature_min": 20,
        "temperature_max": 35,
        "rain_min": 5,
        "rain_max": 15,
        "season_months": [6, 7, 8, 9, 10],
        "elevation_max": 1000,
        "duration_days": 120,
        "stages": [
            {
                "stage": "Land preparation",
                "start_day": 0,
                "end_day": 10,
                "activities": [
                    "Prepare and level the field.",
                    "Ensure suitable soil moisture.",
                ],
            },
            {
                "stage": "Seeding / transplanting",
                "start_day": 11,
                "end_day": 20,
                "activities": [
                    "Sow or transplant healthy seedlings.",
                    "Maintain appropriate field moisture.",
                ],
            },
            {
                "stage": "Establishment",
                "start_day": 21,
                "end_day": 35,
                "activities": [
                    "Monitor germination and plant establishment.",
                    "Control early weeds.",
                ],
            },
            {
                "stage": "Vegetative growth",
                "start_day": 36,
                "end_day": 70,
                "activities": [
                    "Monitor crop growth.",
                    "Apply nutrients according to the crop plan.",
                    "Monitor water requirements.",
                ],
            },
            {
                "stage": "Reproductive stage",
                "start_day": 71,
                "end_day": 100,
                "activities": [
                    "Monitor flowering and panicle development.",
                    "Protect the crop from water and pest stress.",
                ],
            },
            {
                "stage": "Harvest",
                "start_day": 101,
                "end_day": 120,
                "activities": [
                    "Monitor grain maturity.",
                    "Harvest when the crop reaches suitable maturity.",
                ],
            },
        ],
    },

    "Maize": {
        "temperature_min": 18,
        "temperature_max": 32,
        "rain_min": 3,
        "rain_max": 10,
        "season_months": [6, 7, 8, 9, 10],
        "elevation_max": 2000,
        "duration_days": 110,
        "stages": [
            {
                "stage": "Land preparation",
                "start_day": 0,
                "end_day": 7,
                "activities": [
                    "Prepare a well-drained seedbed.",
                    "Remove major weeds and residues.",
                ],
            },
            {
                "stage": "Seeding",
                "start_day": 8,
                "end_day": 14,
                "activities": [
                    "Sow healthy seed at suitable spacing.",
                    "Maintain adequate soil moisture.",
                ],
            },
            {
                "stage": "Germination and establishment",
                "start_day": 15,
                "end_day": 25,
                "activities": [
                    "Monitor germination.",
                    "Check for early pest and weed pressure.",
                ],
            },
            {
                "stage": "Vegetative growth",
                "start_day": 26,
                "end_day": 50,
                "activities": [
                    "Monitor plant growth.",
                    "Apply nutrients according to the crop plan.",
                    "Manage irrigation according to rainfall.",
                ],
            },
            {
                "stage": "Flowering",
                "start_day": 51,
                "end_day": 75,
                "activities": [
                    "Monitor flowering and pollination.",
                    "Avoid severe moisture stress.",
                ],
            },
            {
                "stage": "Grain development",
                "start_day": 76,
                "end_day": 95,
                "activities": [
                    "Monitor grain filling.",
                    "Inspect for pests and disease.",
                ],
            },
            {
                "stage": "Harvest",
                "start_day": 96,
                "end_day": 110,
                "activities": [
                    "Check grain maturity.",
                    "Harvest when crop moisture and maturity are appropriate.",
                ],
            },
        ],
    },

    "Wheat": {
        "temperature_min": 10,
        "temperature_max": 25,
        "rain_min": 1,
        "rain_max": 6,
        "season_months": [10, 11, 12, 1, 2, 3],
        "elevation_max": 3000,
        "duration_days": 120,
        "stages": [
            {
                "stage": "Land preparation",
                "start_day": 0,
                "end_day": 7,
                "activities": [
                    "Prepare a fine and level seedbed.",
                    "Ensure adequate soil moisture.",
                ],
            },
            {
                "stage": "Seeding",
                "start_day": 8,
                "end_day": 14,
                "activities": [
                    "Sow quality seed at suitable spacing.",
                    "Maintain proper seed depth.",
                ],
            },
            {
                "stage": "Germination",
                "start_day": 15,
                "end_day": 25,
                "activities": [
                    "Monitor emergence.",
                    "Inspect early weed pressure.",
                ],
            },
            {
                "stage": "Vegetative growth",
                "start_day": 26,
                "end_day": 60,
                "activities": [
                    "Monitor tillering and crop growth.",
                    "Manage irrigation and nutrients.",
                ],
            },
            {
                "stage": "Flowering",
                "start_day": 61,
                "end_day": 85,
                "activities": [
                    "Monitor flowering.",
                    "Avoid severe water stress.",
                ],
            },
            {
                "stage": "Grain filling",
                "start_day": 86,
                "end_day": 105,
                "activities": [
                    "Monitor grain development.",
                    "Inspect for pests and diseases.",
                ],
            },
            {
                "stage": "Harvest",
                "start_day": 106,
                "end_day": 120,
                "activities": [
                    "Monitor grain maturity.",
                    "Harvest at suitable maturity.",
                ],
            },
        ],
    },

    "Potato": {
        "temperature_min": 10,
        "temperature_max": 25,
        "rain_min": 1,
        "rain_max": 7,
        "season_months": [10, 11, 12, 1, 2],
        "elevation_max": 3000,
        "duration_days": 100,
        "stages": [
            {
                "stage": "Land preparation",
                "start_day": 0,
                "end_day": 7,
                "activities": [
                    "Prepare loose and well-drained soil.",
                    "Create suitable planting beds.",
                ],
            },
            {
                "stage": "Planting",
                "start_day": 8,
                "end_day": 14,
                "activities": [
                    "Plant healthy seed tubers.",
                    "Maintain suitable spacing.",
                ],
            },
            {
                "stage": "Establishment",
                "start_day": 15,
                "end_day": 30,
                "activities": [
                    "Monitor emergence.",
                    "Control early weeds.",
                ],
            },
            {
                "stage": "Vegetative growth",
                "start_day": 31,
                "end_day": 55,
                "activities": [
                    "Monitor canopy growth.",
                    "Manage irrigation and nutrients.",
                ],
            },
            {
                "stage": "Tuber development",
                "start_day": 56,
                "end_day": 80,
                "activities": [
                    "Monitor tuber development.",
                    "Avoid excessive water stress.",
                ],
            },
            {
                "stage": "Maturity",
                "start_day": 81,
                "end_day": 90,
                "activities": [
                    "Monitor crop maturity.",
                    "Reduce unnecessary irrigation near maturity.",
                ],
            },
            {
                "stage": "Harvest",
                "start_day": 91,
                "end_day": 100,
                "activities": [
                    "Harvest mature tubers.",
                    "Handle harvested produce carefully.",
                ],
            },
        ],
    },

    "Tomato": {
        "temperature_min": 18,
        "temperature_max": 30,
        "rain_min": 2,
        "rain_max": 8,
        "season_months": [9, 10, 11, 12, 1, 2],
        "elevation_max": 2000,
        "duration_days": 110,
        "stages": [
            {
                "stage": "Land preparation",
                "start_day": 0,
                "end_day": 10,
                "activities": [
                    "Prepare fertile and well-drained soil.",
                    "Prepare beds and drainage.",
                ],
            },
            {
                "stage": "Transplanting",
                "start_day": 11,
                "end_day": 20,
                "activities": [
                    "Transplant healthy seedlings.",
                    "Provide initial irrigation.",
                ],
            },
            {
                "stage": "Establishment",
                "start_day": 21,
                "end_day": 35,
                "activities": [
                    "Monitor transplant recovery.",
                    "Control weeds.",
                ],
            },
            {
                "stage": "Vegetative growth",
                "start_day": 36,
                "end_day": 60,
                "activities": [
                    "Monitor plant growth.",
                    "Support plants where required.",
                    "Manage irrigation and nutrients.",
                ],
            },
            {
                "stage": "Flowering and fruit set",
                "start_day": 61,
                "end_day": 80,
                "activities": [
                    "Monitor flowering.",
                    "Inspect for pests and diseases.",
                ],
            },
            {
                "stage": "Fruit development",
                "start_day": 81,
                "end_day": 100,
                "activities": [
                    "Monitor fruit development.",
                    "Maintain appropriate moisture.",
                ],
            },
            {
                "stage": "Harvest",
                "start_day": 101,
                "end_day": 110,
                "activities": [
                    "Harvest mature fruits regularly.",
                    "Handle fruits carefully.",
                ],
            },
        ],
    },
}


# =========================================================
# HELPERS
# =========================================================

def clamp(
    value: float,
    minimum: float = 0,
    maximum: float = 100,
) -> int:
    return int(
        round(
            max(
                minimum,
                min(
                    maximum,
                    value,
                ),
            )
        )
    )


def average(
    values: list[float],
) -> float | None:
    if not values:
        return None

    valid = [
        float(value)
        for value in values
        if value is not None
    ]

    if not valid:
        return None

    return sum(valid) / len(valid)


def range_score(
    value: float | None,
    minimum: float,
    maximum: float,
) -> int:
    """
    Returns 100 when value is inside the
    preferred range.

    Gradually decreases outside the range.
    """

    if value is None:
        return 50

    if minimum <= value <= maximum:
        return 100

    distance = (
        minimum - value
        if value < minimum
        else value - maximum
    )

    return clamp(
        100 - (distance * 12)
    )


def rainfall_score(
    rainfall: float | None,
    minimum: float,
    maximum: float,
) -> int:
    if rainfall is None:
        return 50

    if minimum <= rainfall <= maximum:
        return 100

    if rainfall < minimum:
        distance = minimum - rainfall
    else:
        distance = rainfall - maximum

    return clamp(
        100 - (distance * 8)
    )


def season_score(
    month: int,
    suitable_months: list[int],
) -> int:
    if month in suitable_months:
        return 100

    return 55


def vegetation_score(
    ndvi: float | None,
) -> int:
    """
    NDVI is treated as a vegetation indicator,
    not a soil measurement.
    """

    if ndvi is None:
        return 50

    # Typical normalized vegetation interpretation.
    if ndvi >= 0.7:
        return 95

    if ndvi >= 0.5:
        return 85

    if ndvi >= 0.3:
        return 70

    if ndvi >= 0.15:
        return 50

    return 30


def elevation_score(
    elevation: float | None,
    maximum: float,
) -> int:
    if elevation is None:
        return 50

    if elevation <= maximum:
        return 100

    excess = elevation - maximum

    return clamp(
        100 - (excess / 20)
    )


def calculate_crop_score(
    crop: str,
    context: dict[str, Any],
) -> dict[str, int]:

    profile = CROP_PROFILES[crop]

    weather = context.get(
        "weather",
        {},
    )

    current_weather = weather.get(
        "current",
        {},
    )

    forecast = weather.get(
        "seven_day_forecast",
        [],
    )

    current_temperature = (
        current_weather.get(
            "temperature"
        )
    )

    forecast_temperatures = [
        item.get(
            "temperature_max"
        )
        for item in forecast
    ]

    average_forecast_temperature = average(
        [
            value
            for value in forecast_temperatures
            if value is not None
        ]
    )

    temperature_reference = (
        average_forecast_temperature
        if average_forecast_temperature
        is not None
        else current_temperature
    )

    rainfall_values = [
        item.get("rainfall")
        for item in forecast
        if item.get("rainfall") is not None
    ]

    total_rainfall = (
        sum(rainfall_values)
        if rainfall_values
        else None
    )

    rainfall_score_value = rainfall_score(
        total_rainfall,
        profile["rain_min"],
        profile["rain_max"],
    )

    temperature_score_value = range_score(
        temperature_reference,
        profile["temperature_min"],
        profile["temperature_max"],
    )

    current_month = __import__(
        "datetime"
    ).datetime.now().month

    season_score_value = season_score(
        current_month,
        profile["season_months"],
    )

    satellite = context.get(
        "satellite",
        {},
    )

    ndvi = satellite.get(
        "ndvi"
    )

    vegetation_score_value = vegetation_score(
        ndvi
    )

    terrain = context.get(
        "terrain",
        {},
    )

    elevation = terrain.get(
        "elevation_meters"
    )

    terrain_score_value = elevation_score(
        elevation,
        profile["elevation_max"],
    )

    # Soil score is deliberately neutral
    # when laboratory soil data is unavailable.
    soil_score_value = 50

    # Weight:
    #
    # rainfall     25%
    # temperature  30%
    # soil         10%
    # season       15%
    # vegetation   15%
    # terrain       5%
    #
    overall = (
        rainfall_score_value * 0.25
        + temperature_score_value * 0.30
        + soil_score_value * 0.10
        + season_score_value * 0.15
        + vegetation_score_value * 0.15
        + terrain_score_value * 0.05
    )

    return {
        "score": clamp(overall),
        "rainfall_score": rainfall_score_value,
        "temperature_score": temperature_score_value,
        "soil_score": soil_score_value,
        "season_score": season_score_value,
        "vegetation_score": vegetation_score_value,
    }


def build_deterministic_analysis(
    farm_context: dict[str, Any],
) -> dict[str, Any]:

    results = []

    for crop in CROP_PROFILES:
        scores = calculate_crop_score(
            crop,
            farm_context,
        )

        results.append(
            {
                "crop": crop,
                **scores,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    recommended = results[0]

    current_crop = (
        farm_context
        .get("farm", {})
        .get("current_crop")
    )

    current_result = None

    if current_crop:
        for result in results:
            if (
                result["crop"].lower()
                == current_crop.lower()
            ):
                current_result = result
                break

    return {
        "recommended": recommended,
        "current": current_result,
        "all_scores": results,
    }


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are KrishiMap AI.

You are an agricultural decision-support
assistant for Indian farmers.

You receive farm data, deterministic crop
scores, weather data, satellite indicators,
terrain information and a seven-day forecast.

You MUST reason only from supplied data.

==================================================
CRITICAL DATA RULES
==================================================

1. Never invent weather values.

2. Never invent satellite values.

3. Never invent elevation.

4. Never invent soil measurements.

5. If a value is null or unavailable,
   explicitly say that the data is unavailable.

6. Sentinel-2 indicators are remote-sensing
   proxies.

7. NDVI is a vegetation-health indicator.

8. NDMI is a vegetation-water indicator.

9. BSI is a bare-soil spectral indicator.

10. Do NOT describe NDVI, NDMI or BSI as
    laboratory NPK, pH or direct soil measurements.

11. Elevation is only an elevation/terrain
    indicator. It is NOT a complete terrain survey.

12. The seven-day forecast must be considered
    when discussing irrigation, rainfall risk,
    field operations and crop suitability.

13. Do not change deterministic scores supplied
    in the context.

14. Do not invent alternative scores.

15. The recommended crop is already selected
    by the backend.

==================================================
LANGUAGE
==================================================

language = "en"
language = "hi"
language = "bn"

en -> English
hi -> Hindi
bn -> Bengali

ALL farmer-facing text must be written in
the requested language.

Crop names may remain in their standard
English names when appropriate.

==================================================
INTENDED CROP
==================================================

farm.current_crop is the farmer's intended
or current crop.

Compare it with the backend-selected
recommended crop.

If current_crop is null:

Say that no intended crop was provided.

==================================================
SCHEDULE
==================================================

Use the supplied crop schedule.

Do not invent a completely different
growth duration.

You may rewrite activity descriptions
in the requested language.

Do not create exact calendar dates.

Use relative day ranges only.

==================================================
WEATHER RISK
==================================================

Use the seven-day forecast.

Mention rainfall or temperature risks
only when supported by the supplied data.

Do not invent extreme-weather events.

==================================================
SATELLITE
==================================================

Use NDVI, NDMI and BSI only as
remote-sensing indicators.

If unavailable, clearly state that
satellite observations are unavailable.

==================================================
SOIL
==================================================

If laboratory soil data is unavailable,
do NOT pretend to know NPK, pH or
specific soil nutrient values.

==================================================
OUTPUT
==================================================

Return ONLY valid JSON.

Do not use markdown.

Do not use code fences.

Return exactly:

{
  "language": "en",
  "intended_crop": null,
  "recommended_crop": "Maize",
  "recommendation_score": 86,
  "why_recommended": "string",
  "comparison": [
    {
      "crop": "Rice",
      "score": 78,
      "reason": "string"
    }
  ],
  "farm_insights": [
    "string"
  ],
  "weather_risk": [
    "string"
  ],
  "satellite_insights": [
    "string"
  ],
  "terrain_insights": [
    "string"
  ],
  "schedule": [
    {
      "stage": "Seeding",
      "start_day": 0,
      "end_day": 7,
      "activities": [
        "string"
      ]
    }
  ],
  "farmer_advice": [
    "string"
  ],
  "explanation": "string"
}
""",
        ),
        (
            "human",
            """
Requested language:

{language}

Farm intelligence context:

{farm_context}

Deterministic backend analysis:

{deterministic_analysis}

Generate the farmer-facing interpretation.

Remember:

- Do not change numeric scores.
- Do not invent measurements.
- Do not invent soil values.
- Do not invent satellite values.
- Use the seven-day forecast.
- Compare intended/current crop with recommended crop.
- Use the supplied crop schedule.
- Return only valid JSON.
""",
        ),
    ]
)


chain = prompt | llm


# =========================================================
# MAIN AI FUNCTION
# =========================================================

def get_crop_recommendation(
    farm_context: dict,
    language: str = "en",
) -> dict:

    if language not in {
        "en",
        "hi",
        "bn",
    }:
        language = "en"

    deterministic_analysis = (
        build_deterministic_analysis(
            farm_context
        )
    )

    response = chain.invoke(
        {
            "language": language,

            "farm_context": json.dumps(
                farm_context,
                indent=2,
                ensure_ascii=False,
            ),

            "deterministic_analysis": json.dumps(
                deterministic_analysis,
                indent=2,
                ensure_ascii=False,
            ),
        }
    )

    content = response.content

    if not isinstance(
        content,
        str,
    ):
        content = str(content)

    content = content.strip()

    # -----------------------------------------------------
    # Remove accidental markdown fences.
    # -----------------------------------------------------

    if content.startswith("```"):
        content = content.replace(
            "```json",
            "",
        )

        content = content.replace(
            "```",
            "",
        )

        content = content.strip()

    try:
        ai_result = json.loads(
            content
        )

    except json.JSONDecodeError as exc:
        print(
            "Invalid AI JSON:",
            content,
        )

        raise ValueError(
            "AI returned invalid JSON"
        ) from exc

    # -----------------------------------------------------
    # Backend is the authority for scores.
    #
    # Never trust the LLM to modify them.
    # -----------------------------------------------------

    recommended = (
        deterministic_analysis[
            "recommended"
        ]
    )

    all_scores = (
        deterministic_analysis[
            "all_scores"
        ]
    )

    current = (
        deterministic_analysis[
            "current"
        ]
    )

    current_crop = (
        farm_context
        .get("farm", {})
        .get("current_crop")
    )

    comparison = []

    ai_comparison = {
        item.get("crop"): item
        for item in (
            ai_result.get(
                "comparison",
                []
            )
        )
        if item.get("crop")
    }

    for result in all_scores:
        crop_name = result["crop"]

        ai_item = ai_comparison.get(
            crop_name
        )

        comparison.append(
            {
                "crop": crop_name,
                "score": result["score"],
                "reason": (
                    ai_item.get("reason")
                    if ai_item
                    else (
                        f"Backend suitability score: "
                        f"{result['score']}."
                    )
                ),
            }
        )

    # -----------------------------------------------------
    # Select deterministic schedule.
    # -----------------------------------------------------

    recommended_crop = (
        recommended["crop"]
    )

    schedule = CROP_PROFILES[
        recommended_crop
    ]["stages"]

    # -----------------------------------------------------
    # Final response.
    # -----------------------------------------------------

    return {
        "language": language,

        "intended_crop": current_crop,

        "recommended_crop":
            recommended_crop,

        "recommendation_score":
            recommended["score"],

        "why_recommended":
            ai_result.get(
                "why_recommended",
                ai_result.get(
                    "explanation",
                    "",
                ),
            ),

        "comparison":
            comparison,

        "farm_insights":
            ai_result.get(
                "farm_insights",
                [],
            ),

        "weather_risk":
            ai_result.get(
                "weather_risk",
                [],
            ),

        "satellite_insights":
            ai_result.get(
                "satellite_insights",
                [],
            ),

        "terrain_insights":
            ai_result.get(
                "terrain_insights",
                [],
            ),

        "schedule":
            schedule,

        "farmer_advice":
            ai_result.get(
                "farmer_advice",
                [],
            ),

        "explanation":
            ai_result.get(
                "explanation",
                "",
            ),

        # Backward compatibility with
        # the existing frontend.
        "crop":
            recommended_crop,

        "suitability_score":
            recommended["score"],

        "rainfall_score":
            recommended[
                "rainfall_score"
            ],

        "temperature_score":
            recommended[
                "temperature_score"
            ],

        "soil_score":
            recommended[
                "soil_score"
            ],

        "season_score":
            recommended[
                "season_score"
            ],

        "vegetation_score":
            recommended[
                "vegetation_score"
            ],
    }