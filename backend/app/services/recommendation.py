
# # import json
# # import os
# # from typing import Any

# # from dotenv import load_dotenv
# # from langchain_core.prompts import ChatPromptTemplate
# # from langchain_groq import ChatGroq


# # load_dotenv()


# # GROQ_API_KEY = os.getenv(
# #     "GROQ_API_KEY"
# # )

# # GROQ_MODEL = os.getenv(
# #     "GROQ_MODEL",
# #     "llama-3.3-70b-versatile",
# # )


# # if not GROQ_API_KEY:
# #     raise RuntimeError(
# #         "GROQ_API_KEY is not configured"
# #     )


# # llm = ChatGroq(
# #     api_key=GROQ_API_KEY,
# #     model=GROQ_MODEL,
# #     temperature=0.1,
# # )


# # # =========================================================
# # # CROP KNOWLEDGE
# # # =========================================================

# # CROP_PROFILES: dict[str, dict[str, Any]] = {
# #     "Rice": {
# #         "temperature_min": 20,
# #         "temperature_max": 35,
# #         "rain_min": 5,
# #         "rain_max": 15,
# #         "season_months": [6, 7, 8, 9, 10],
# #         "elevation_max": 1000,
# #         "duration_days": 120,
# #         "stages": [
# #             {
# #                 "stage": "Land preparation",
# #                 "start_day": 0,
# #                 "end_day": 10,
# #                 "activities": [
# #                     "Prepare and level the field.",
# #                     "Ensure suitable soil moisture.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Seeding / transplanting",
# #                 "start_day": 11,
# #                 "end_day": 20,
# #                 "activities": [
# #                     "Sow or transplant healthy seedlings.",
# #                     "Maintain appropriate field moisture.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Establishment",
# #                 "start_day": 21,
# #                 "end_day": 35,
# #                 "activities": [
# #                     "Monitor germination and plant establishment.",
# #                     "Control early weeds.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Vegetative growth",
# #                 "start_day": 36,
# #                 "end_day": 70,
# #                 "activities": [
# #                     "Monitor crop growth.",
# #                     "Apply nutrients according to the crop plan.",
# #                     "Monitor water requirements.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Reproductive stage",
# #                 "start_day": 71,
# #                 "end_day": 100,
# #                 "activities": [
# #                     "Monitor flowering and panicle development.",
# #                     "Protect the crop from water and pest stress.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Harvest",
# #                 "start_day": 101,
# #                 "end_day": 120,
# #                 "activities": [
# #                     "Monitor grain maturity.",
# #                     "Harvest when the crop reaches suitable maturity.",
# #                 ],
# #             },
# #         ],
# #     },

# #     "Maize": {
# #         "temperature_min": 18,
# #         "temperature_max": 32,
# #         "rain_min": 3,
# #         "rain_max": 10,
# #         "season_months": [6, 7, 8, 9, 10],
# #         "elevation_max": 2000,
# #         "duration_days": 110,
# #         "stages": [
# #             {
# #                 "stage": "Land preparation",
# #                 "start_day": 0,
# #                 "end_day": 7,
# #                 "activities": [
# #                     "Prepare a well-drained seedbed.",
# #                     "Remove major weeds and residues.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Seeding",
# #                 "start_day": 8,
# #                 "end_day": 14,
# #                 "activities": [
# #                     "Sow healthy seed at suitable spacing.",
# #                     "Maintain adequate soil moisture.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Germination and establishment",
# #                 "start_day": 15,
# #                 "end_day": 25,
# #                 "activities": [
# #                     "Monitor germination.",
# #                     "Check for early pest and weed pressure.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Vegetative growth",
# #                 "start_day": 26,
# #                 "end_day": 50,
# #                 "activities": [
# #                     "Monitor plant growth.",
# #                     "Apply nutrients according to the crop plan.",
# #                     "Manage irrigation according to rainfall.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Flowering",
# #                 "start_day": 51,
# #                 "end_day": 75,
# #                 "activities": [
# #                     "Monitor flowering and pollination.",
# #                     "Avoid severe moisture stress.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Grain development",
# #                 "start_day": 76,
# #                 "end_day": 95,
# #                 "activities": [
# #                     "Monitor grain filling.",
# #                     "Inspect for pests and disease.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Harvest",
# #                 "start_day": 96,
# #                 "end_day": 110,
# #                 "activities": [
# #                     "Check grain maturity.",
# #                     "Harvest when crop moisture and maturity are appropriate.",
# #                 ],
# #             },
# #         ],
# #     },

# #     "Wheat": {
# #         "temperature_min": 10,
# #         "temperature_max": 25,
# #         "rain_min": 1,
# #         "rain_max": 6,
# #         "season_months": [10, 11, 12, 1, 2, 3],
# #         "elevation_max": 3000,
# #         "duration_days": 120,
# #         "stages": [
# #             {
# #                 "stage": "Land preparation",
# #                 "start_day": 0,
# #                 "end_day": 7,
# #                 "activities": [
# #                     "Prepare a fine and level seedbed.",
# #                     "Ensure adequate soil moisture.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Seeding",
# #                 "start_day": 8,
# #                 "end_day": 14,
# #                 "activities": [
# #                     "Sow quality seed at suitable spacing.",
# #                     "Maintain proper seed depth.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Germination",
# #                 "start_day": 15,
# #                 "end_day": 25,
# #                 "activities": [
# #                     "Monitor emergence.",
# #                     "Inspect early weed pressure.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Vegetative growth",
# #                 "start_day": 26,
# #                 "end_day": 60,
# #                 "activities": [
# #                     "Monitor tillering and crop growth.",
# #                     "Manage irrigation and nutrients.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Flowering",
# #                 "start_day": 61,
# #                 "end_day": 85,
# #                 "activities": [
# #                     "Monitor flowering.",
# #                     "Avoid severe water stress.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Grain filling",
# #                 "start_day": 86,
# #                 "end_day": 105,
# #                 "activities": [
# #                     "Monitor grain development.",
# #                     "Inspect for pests and diseases.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Harvest",
# #                 "start_day": 106,
# #                 "end_day": 120,
# #                 "activities": [
# #                     "Monitor grain maturity.",
# #                     "Harvest at suitable maturity.",
# #                 ],
# #             },
# #         ],
# #     },

# #     "Potato": {
# #         "temperature_min": 10,
# #         "temperature_max": 25,
# #         "rain_min": 1,
# #         "rain_max": 7,
# #         "season_months": [10, 11, 12, 1, 2],
# #         "elevation_max": 3000,
# #         "duration_days": 100,
# #         "stages": [
# #             {
# #                 "stage": "Land preparation",
# #                 "start_day": 0,
# #                 "end_day": 7,
# #                 "activities": [
# #                     "Prepare loose and well-drained soil.",
# #                     "Create suitable planting beds.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Planting",
# #                 "start_day": 8,
# #                 "end_day": 14,
# #                 "activities": [
# #                     "Plant healthy seed tubers.",
# #                     "Maintain suitable spacing.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Establishment",
# #                 "start_day": 15,
# #                 "end_day": 30,
# #                 "activities": [
# #                     "Monitor emergence.",
# #                     "Control early weeds.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Vegetative growth",
# #                 "start_day": 31,
# #                 "end_day": 55,
# #                 "activities": [
# #                     "Monitor canopy growth.",
# #                     "Manage irrigation and nutrients.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Tuber development",
# #                 "start_day": 56,
# #                 "end_day": 80,
# #                 "activities": [
# #                     "Monitor tuber development.",
# #                     "Avoid excessive water stress.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Maturity",
# #                 "start_day": 81,
# #                 "end_day": 90,
# #                 "activities": [
# #                     "Monitor crop maturity.",
# #                     "Reduce unnecessary irrigation near maturity.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Harvest",
# #                 "start_day": 91,
# #                 "end_day": 100,
# #                 "activities": [
# #                     "Harvest mature tubers.",
# #                     "Handle harvested produce carefully.",
# #                 ],
# #             },
# #         ],
# #     },

# #     "Tomato": {
# #         "temperature_min": 18,
# #         "temperature_max": 30,
# #         "rain_min": 2,
# #         "rain_max": 8,
# #         "season_months": [9, 10, 11, 12, 1, 2],
# #         "elevation_max": 2000,
# #         "duration_days": 110,
# #         "stages": [
# #             {
# #                 "stage": "Land preparation",
# #                 "start_day": 0,
# #                 "end_day": 10,
# #                 "activities": [
# #                     "Prepare fertile and well-drained soil.",
# #                     "Prepare beds and drainage.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Transplanting",
# #                 "start_day": 11,
# #                 "end_day": 20,
# #                 "activities": [
# #                     "Transplant healthy seedlings.",
# #                     "Provide initial irrigation.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Establishment",
# #                 "start_day": 21,
# #                 "end_day": 35,
# #                 "activities": [
# #                     "Monitor transplant recovery.",
# #                     "Control weeds.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Vegetative growth",
# #                 "start_day": 36,
# #                 "end_day": 60,
# #                 "activities": [
# #                     "Monitor plant growth.",
# #                     "Support plants where required.",
# #                     "Manage irrigation and nutrients.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Flowering and fruit set",
# #                 "start_day": 61,
# #                 "end_day": 80,
# #                 "activities": [
# #                     "Monitor flowering.",
# #                     "Inspect for pests and diseases.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Fruit development",
# #                 "start_day": 81,
# #                 "end_day": 100,
# #                 "activities": [
# #                     "Monitor fruit development.",
# #                     "Maintain appropriate moisture.",
# #                 ],
# #             },
# #             {
# #                 "stage": "Harvest",
# #                 "start_day": 101,
# #                 "end_day": 110,
# #                 "activities": [
# #                     "Harvest mature fruits regularly.",
# #                     "Handle fruits carefully.",
# #                 ],
# #             },
# #         ],
# #     },
# # }


# # # =========================================================
# # # HELPERS
# # # =========================================================

# # def clamp(
# #     value: float,
# #     minimum: float = 0,
# #     maximum: float = 100,
# # ) -> int:
# #     return int(
# #         round(
# #             max(
# #                 minimum,
# #                 min(
# #                     maximum,
# #                     value,
# #                 ),
# #             )
# #         )
# #     )


# # def average(
# #     values: list[float],
# # ) -> float | None:
# #     if not values:
# #         return None

# #     valid = [
# #         float(value)
# #         for value in values
# #         if value is not None
# #     ]

# #     if not valid:
# #         return None

# #     return sum(valid) / len(valid)


# # def range_score(
# #     value: float | None,
# #     minimum: float,
# #     maximum: float,
# # ) -> int:
# #     """
# #     Returns 100 when value is inside the
# #     preferred range.

# #     Gradually decreases outside the range.
# #     """

# #     if value is None:
# #         return 50

# #     if minimum <= value <= maximum:
# #         return 100

# #     distance = (
# #         minimum - value
# #         if value < minimum
# #         else value - maximum
# #     )

# #     return clamp(
# #         100 - (distance * 12)
# #     )


# # def rainfall_score(
# #     rainfall: float | None,
# #     minimum: float,
# #     maximum: float,
# # ) -> int:
# #     if rainfall is None:
# #         return 50

# #     if minimum <= rainfall <= maximum:
# #         return 100

# #     if rainfall < minimum:
# #         distance = minimum - rainfall
# #     else:
# #         distance = rainfall - maximum

# #     return clamp(
# #         100 - (distance * 8)
# #     )


# # def season_score(
# #     month: int,
# #     suitable_months: list[int],
# # ) -> int:
# #     if month in suitable_months:
# #         return 100

# #     return 55


# # def vegetation_score(
# #     ndvi: float | None,
# # ) -> int:
# #     """
# #     NDVI is treated as a vegetation indicator,
# #     not a soil measurement.
# #     """

# #     if ndvi is None:
# #         return 50

# #     # Typical normalized vegetation interpretation.
# #     if ndvi >= 0.7:
# #         return 95

# #     if ndvi >= 0.5:
# #         return 85

# #     if ndvi >= 0.3:
# #         return 70

# #     if ndvi >= 0.15:
# #         return 50

# #     return 30


# # def elevation_score(
# #     elevation: float | None,
# #     maximum: float,
# # ) -> int:
# #     if elevation is None:
# #         return 50

# #     if elevation <= maximum:
# #         return 100

# #     excess = elevation - maximum

# #     return clamp(
# #         100 - (excess / 20)
# #     )


# # def calculate_crop_score(
# #     crop: str,
# #     context: dict[str, Any],
# # ) -> dict[str, int]:

# #     profile = CROP_PROFILES[crop]

# #     weather = context.get(
# #         "weather",
# #         {},
# #     )

# #     current_weather = weather.get(
# #         "current",
# #         {},
# #     )

# #     forecast = weather.get(
# #         "seven_day_forecast",
# #         [],
# #     )

# #     current_temperature = (
# #         current_weather.get(
# #             "temperature"
# #         )
# #     )

# #     forecast_temperatures = [
# #         item.get(
# #             "temperature_max"
# #         )
# #         for item in forecast
# #     ]

# #     average_forecast_temperature = average(
# #         [
# #             value
# #             for value in forecast_temperatures
# #             if value is not None
# #         ]
# #     )

# #     temperature_reference = (
# #         average_forecast_temperature
# #         if average_forecast_temperature
# #         is not None
# #         else current_temperature
# #     )

# #     rainfall_values = [
# #         item.get("rainfall")
# #         for item in forecast
# #         if item.get("rainfall") is not None
# #     ]

# #     total_rainfall = (
# #         sum(rainfall_values)
# #         if rainfall_values
# #         else None
# #     )

# #     rainfall_score_value = rainfall_score(
# #         total_rainfall,
# #         profile["rain_min"],
# #         profile["rain_max"],
# #     )

# #     temperature_score_value = range_score(
# #         temperature_reference,
# #         profile["temperature_min"],
# #         profile["temperature_max"],
# #     )

# #     current_month = __import__(
# #         "datetime"
# #     ).datetime.now().month

# #     season_score_value = season_score(
# #         current_month,
# #         profile["season_months"],
# #     )

# #     satellite = context.get(
# #         "satellite",
# #         {},
# #     )

# #     ndvi = satellite.get(
# #         "ndvi"
# #     )

# #     vegetation_score_value = vegetation_score(
# #         ndvi
# #     )

# #     terrain = context.get(
# #         "terrain",
# #         {},
# #     )

# #     elevation = terrain.get(
# #         "elevation_meters"
# #     )

# #     terrain_score_value = elevation_score(
# #         elevation,
# #         profile["elevation_max"],
# #     )

# #     # Soil score is deliberately neutral
# #     # when laboratory soil data is unavailable.
# #     soil_score_value = 50

# #     # Weight:
# #     #
# #     # rainfall     25%
# #     # temperature  30%
# #     # soil         10%
# #     # season       15%
# #     # vegetation   15%
# #     # terrain       5%
# #     #
# #     overall = (
# #         rainfall_score_value * 0.25
# #         + temperature_score_value * 0.30
# #         + soil_score_value * 0.10
# #         + season_score_value * 0.15
# #         + vegetation_score_value * 0.15
# #         + terrain_score_value * 0.05
# #     )

# #     return {
# #         "score": clamp(overall),
# #         "rainfall_score": rainfall_score_value,
# #         "temperature_score": temperature_score_value,
# #         "soil_score": soil_score_value,
# #         "season_score": season_score_value,
# #         "vegetation_score": vegetation_score_value,
# #     }


# # def build_deterministic_analysis(
# #     farm_context: dict[str, Any],
# # ) -> dict[str, Any]:

# #     results = []

# #     for crop in CROP_PROFILES:
# #         scores = calculate_crop_score(
# #             crop,
# #             farm_context,
# #         )

# #         results.append(
# #             {
# #                 "crop": crop,
# #                 **scores,
# #             }
# #         )

# #     results.sort(
# #         key=lambda item: item["score"],
# #         reverse=True,
# #     )

# #     recommended = results[0]

# #     current_crop = (
# #         farm_context
# #         .get("farm", {})
# #         .get("current_crop")
# #     )

# #     current_result = None

# #     if current_crop:
# #         for result in results:
# #             if (
# #                 result["crop"].lower()
# #                 == current_crop.lower()
# #             ):
# #                 current_result = result
# #                 break

# #     return {
# #         "recommended": recommended,
# #         "current": current_result,
# #         "all_scores": results,
# #     }


# # # =========================================================
# # # PROMPT
# # # =========================================================

# # prompt = ChatPromptTemplate.from_messages(
# #     [
# #         (
# #             "system",
# #             """
# # You are KrishiMap AI.

# # You are an agricultural decision-support
# # assistant for Indian farmers.

# # You receive farm data, deterministic crop
# # scores, weather data, satellite indicators,
# # terrain information and a seven-day forecast.

# # You MUST reason only from supplied data.

# # ==================================================
# # CRITICAL DATA RULES
# # ==================================================

# # 1. Never invent weather values.

# # 2. Never invent satellite values.

# # 3. Never invent elevation.

# # 4. Never invent soil measurements.

# # 5. If a value is null or unavailable,
# #    explicitly say that the data is unavailable.

# # 6. Sentinel-2 indicators are remote-sensing
# #    proxies.

# # 7. NDVI is a vegetation-health indicator.

# # 8. NDMI is a vegetation-water indicator.

# # 9. BSI is a bare-soil spectral indicator.

# # 10. Do NOT describe NDVI, NDMI or BSI as
# #     laboratory NPK, pH or direct soil measurements.

# # 11. Elevation is only an elevation/terrain
# #     indicator. It is NOT a complete terrain survey.

# # 12. The seven-day forecast must be considered
# #     when discussing irrigation, rainfall risk,
# #     field operations and crop suitability.

# # 13. Do not change deterministic scores supplied
# #     in the context.

# # 14. Do not invent alternative scores.

# # 15. The recommended crop is already selected
# #     by the backend.

# # ==================================================
# # LANGUAGE
# # ==================================================

# # language = "en"
# # language = "hi"
# # language = "bn"

# # en -> English
# # hi -> Hindi
# # bn -> Bengali

# # ALL farmer-facing text must be written in
# # the requested language.

# # Crop names may remain in their standard
# # English names when appropriate.

# # ==================================================
# # INTENDED CROP
# # ==================================================

# # farm.current_crop is the farmer's intended
# # or current crop.

# # Compare it with the backend-selected
# # recommended crop.

# # If current_crop is null:

# # Say that no intended crop was provided.

# # ==================================================
# # SCHEDULE
# # ==================================================

# # Use the supplied crop schedule.

# # Do not invent a completely different
# # growth duration.

# # You may rewrite activity descriptions
# # in the requested language.

# # Do not create exact calendar dates.

# # Use relative day ranges only.

# # ==================================================
# # WEATHER RISK
# # ==================================================

# # Use the seven-day forecast.

# # Mention rainfall or temperature risks
# # only when supported by the supplied data.

# # Do not invent extreme-weather events.

# # ==================================================
# # SATELLITE
# # ==================================================

# # Use NDVI, NDMI and BSI only as
# # remote-sensing indicators.

# # If unavailable, clearly state that
# # satellite observations are unavailable.

# # ==================================================
# # SOIL
# # ==================================================

# # If laboratory soil data is unavailable,
# # do NOT pretend to know NPK, pH or
# # specific soil nutrient values.

# # ==================================================
# # OUTPUT
# # ==================================================

# # Return ONLY valid JSON.

# # Do not use markdown.

# # Do not use code fences.

# # Return exactly:

# # {
# #   "language": "en",
# #   "intended_crop": null,
# #   "recommended_crop": "Maize",
# #   "recommendation_score": 86,
# #   "why_recommended": "string",
# #   "comparison": [
# #     {
# #       "crop": "Rice",
# #       "score": 78,
# #       "reason": "string"
# #     }
# #   ],
# #   "farm_insights": [
# #     "string"
# #   ],
# #   "weather_risk": [
# #     "string"
# #   ],
# #   "satellite_insights": [
# #     "string"
# #   ],
# #   "terrain_insights": [
# #     "string"
# #   ],
# #   "schedule": [
# #     {
# #       "stage": "Seeding",
# #       "start_day": 0,
# #       "end_day": 7,
# #       "activities": [
# #         "string"
# #       ]
# #     }
# #   ],
# #   "farmer_advice": [
# #     "string"
# #   ],
# #   "explanation": "string"
# # }
# # """,
# #         ),
# #         (
# #             "human",
# #             """
# # Requested language:

# # {language}

# # Farm intelligence context:

# # {farm_context}

# # Deterministic backend analysis:

# # {deterministic_analysis}

# # Generate the farmer-facing interpretation.

# # Remember:

# # - Do not change numeric scores.
# # - Do not invent measurements.
# # - Do not invent soil values.
# # - Do not invent satellite values.
# # - Use the seven-day forecast.
# # - Compare intended/current crop with recommended crop.
# # - Use the supplied crop schedule.
# # - Return only valid JSON.
# # """,
# #         ),
# #     ]
# # )


# # chain = prompt | llm


# # # =========================================================
# # # MAIN AI FUNCTION
# # # =========================================================

# # def get_crop_recommendation(
# #     farm_context: dict,
# #     language: str = "en",
# # ) -> dict:

# #     if language not in {
# #         "en",
# #         "hi",
# #         "bn",
# #     }:
# #         language = "en"

# #     deterministic_analysis = (
# #         build_deterministic_analysis(
# #             farm_context
# #         )
# #     )

# #     response = chain.invoke(
# #         {
# #             "language": language,

# #             "farm_context": json.dumps(
# #                 farm_context,
# #                 indent=2,
# #                 ensure_ascii=False,
# #             ),

# #             "deterministic_analysis": json.dumps(
# #                 deterministic_analysis,
# #                 indent=2,
# #                 ensure_ascii=False,
# #             ),
# #         }
# #     )

# #     content = response.content

# #     if not isinstance(
# #         content,
# #         str,
# #     ):
# #         content = str(content)

# #     content = content.strip()

# #     # -----------------------------------------------------
# #     # Remove accidental markdown fences.
# #     # -----------------------------------------------------

# #     if content.startswith("```"):
# #         content = content.replace(
# #             "```json",
# #             "",
# #         )

# #         content = content.replace(
# #             "```",
# #             "",
# #         )

# #         content = content.strip()

# #     try:
# #         ai_result = json.loads(
# #             content
# #         )

# #     except json.JSONDecodeError as exc:
# #         print(
# #             "Invalid AI JSON:",
# #             content,
# #         )

# #         raise ValueError(
# #             "AI returned invalid JSON"
# #         ) from exc

# #     # -----------------------------------------------------
# #     # Backend is the authority for scores.
# #     #
# #     # Never trust the LLM to modify them.
# #     # -----------------------------------------------------

# #     recommended = (
# #         deterministic_analysis[
# #             "recommended"
# #         ]
# #     )

# #     all_scores = (
# #         deterministic_analysis[
# #             "all_scores"
# #         ]
# #     )

# #     current = (
# #         deterministic_analysis[
# #             "current"
# #         ]
# #     )

# #     current_crop = (
# #         farm_context
# #         .get("farm", {})
# #         .get("current_crop")
# #     )

# #     comparison = []

# #     ai_comparison = {
# #         item.get("crop"): item
# #         for item in (
# #             ai_result.get(
# #                 "comparison",
# #                 []
# #             )
# #         )
# #         if item.get("crop")
# #     }

# #     for result in all_scores:
# #         crop_name = result["crop"]

# #         ai_item = ai_comparison.get(
# #             crop_name
# #         )

# #         comparison.append(
# #             {
# #                 "crop": crop_name,
# #                 "score": result["score"],
# #                 "reason": (
# #                     ai_item.get("reason")
# #                     if ai_item
# #                     else (
# #                         f"Backend suitability score: "
# #                         f"{result['score']}."
# #                     )
# #                 ),
# #             }
# #         )

# #     # -----------------------------------------------------
# #     # Select deterministic schedule.
# #     # -----------------------------------------------------

# #     recommended_crop = (
# #         recommended["crop"]
# #     )

# #     schedule = CROP_PROFILES[
# #         recommended_crop
# #     ]["stages"]

# #     # -----------------------------------------------------
# #     # Final response.
# #     # -----------------------------------------------------

# #     return {
# #         "language": language,

# #         "intended_crop": current_crop,

# #         "recommended_crop":
# #             recommended_crop,

# #         "recommendation_score":
# #             recommended["score"],

# #         "why_recommended":
# #             ai_result.get(
# #                 "why_recommended",
# #                 ai_result.get(
# #                     "explanation",
# #                     "",
# #                 ),
# #             ),

# #         "comparison":
# #             comparison,

# #         "farm_insights":
# #             ai_result.get(
# #                 "farm_insights",
# #                 [],
# #             ),

# #         "weather_risk":
# #             ai_result.get(
# #                 "weather_risk",
# #                 [],
# #             ),

# #         "satellite_insights":
# #             ai_result.get(
# #                 "satellite_insights",
# #                 [],
# #             ),

# #         "terrain_insights":
# #             ai_result.get(
# #                 "terrain_insights",
# #                 [],
# #             ),

# #         "schedule":
# #             schedule,

# #         "farmer_advice":
# #             ai_result.get(
# #                 "farmer_advice",
# #                 [],
# #             ),

# #         "explanation":
# #             ai_result.get(
# #                 "explanation",
# #                 "",
# #             ),

# #         # Backward compatibility with
# #         # the existing frontend.
# #         "crop":
# #             recommended_crop,

# #         "suitability_score":
# #             recommended["score"],

# #         "rainfall_score":
# #             recommended[
# #                 "rainfall_score"
# #             ],

# #         "temperature_score":
# #             recommended[
# #                 "temperature_score"
# #             ],

# #         "soil_score":
# #             recommended[
# #                 "soil_score"
# #             ],

# #         "season_score":
# #             recommended[
# #                 "season_score"
# #             ],

# #         "vegetation_score":
# #             recommended[
# #                 "vegetation_score"
# #             ],
# #     }
# import json
# import logging
# import os
# from datetime import datetime, timezone
# from typing import Any

# from dotenv import load_dotenv
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq

# load_dotenv()

# logger = logging.getLogger("krishimap.recommendation")


# # ============================================================
# # CONFIGURATION
# # ============================================================

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_MODEL = os.getenv(
#     "GROQ_MODEL",
#     "llama-3.3-70b-versatile",
# )

# SUPPORTED_LANGUAGES = {
#     "en",
#     "hi",
#     "bn",
# }


# # ============================================================
# # CROP PROFILES
# # ============================================================

# CROP_PROFILES: dict[str, dict[str, Any]] = {
#     "Rice": {
#         "temperature_min": 20,
#         "temperature_max": 35,
#         "rain_min": 100,
#         "rain_max": 300,
#         "season_months": [6, 7, 8, 9, 10],
#         "elevation_max": 500,
#         "duration_days": 120,
#         "stages": [
#             {
#                 "stage": "Land Preparation",
#                 "start_day": 1,
#                 "end_day": 10,
#                 "activities": [
#                     "Prepare and level the field",
#                     "Ensure adequate soil moisture",
#                 ],
#             },
#             {
#                 "stage": "Sowing / Transplanting",
#                 "start_day": 11,
#                 "end_day": 25,
#                 "activities": [
#                     "Sow or transplant healthy seedlings",
#                     "Maintain suitable water level",
#                 ],
#             },
#             {
#                 "stage": "Vegetative Growth",
#                 "start_day": 26,
#                 "end_day": 60,
#                 "activities": [
#                     "Monitor weeds",
#                     "Apply nutrients according to soil requirements",
#                 ],
#             },
#             {
#                 "stage": "Reproductive Growth",
#                 "start_day": 61,
#                 "end_day": 95,
#                 "activities": [
#                     "Monitor pests and diseases",
#                     "Maintain adequate moisture",
#                 ],
#             },
#             {
#                 "stage": "Maturity and Harvest",
#                 "start_day": 96,
#                 "end_day": 120,
#                 "activities": [
#                     "Reduce irrigation near maturity",
#                     "Harvest when grains reach suitable maturity",
#                 ],
#             },
#         ],
#     },

#     "Maize": {
#         "temperature_min": 18,
#         "temperature_max": 32,
#         "rain_min": 50,
#         "rain_max": 150,
#         "season_months": [6, 7, 8, 9, 10],
#         "elevation_max": 2000,
#         "duration_days": 100,
#         "stages": [
#             {
#                 "stage": "Land Preparation",
#                 "start_day": 1,
#                 "end_day": 10,
#                 "activities": [
#                     "Prepare a well-drained seedbed",
#                     "Remove weeds and crop residues",
#                 ],
#             },
#             {
#                 "stage": "Sowing",
#                 "start_day": 11,
#                 "end_day": 15,
#                 "activities": [
#                     "Sow quality seeds",
#                     "Maintain appropriate plant spacing",
#                 ],
#             },
#             {
#                 "stage": "Vegetative Growth",
#                 "start_day": 16,
#                 "end_day": 45,
#                 "activities": [
#                     "Control weeds",
#                     "Monitor early pest pressure",
#                 ],
#             },
#             {
#                 "stage": "Flowering and Grain Filling",
#                 "start_day": 46,
#                 "end_day": 80,
#                 "activities": [
#                     "Monitor moisture",
#                     "Monitor pests and diseases",
#                 ],
#             },
#             {
#                 "stage": "Maturity and Harvest",
#                 "start_day": 81,
#                 "end_day": 100,
#                 "activities": [
#                     "Allow grain to mature",
#                     "Harvest at suitable moisture",
#                 ],
#             },
#         ],
#     },

#     "Wheat": {
#         "temperature_min": 10,
#         "temperature_max": 25,
#         "rain_min": 20,
#         "rain_max": 80,
#         "season_months": [10, 11, 12, 1, 2],
#         "elevation_max": 1500,
#         "duration_days": 120,
#         "stages": [
#             {
#                 "stage": "Land Preparation",
#                 "start_day": 1,
#                 "end_day": 10,
#                 "activities": [
#                     "Prepare a fine seedbed",
#                     "Ensure proper drainage",
#                 ],
#             },
#             {
#                 "stage": "Sowing",
#                 "start_day": 11,
#                 "end_day": 15,
#                 "activities": [
#                     "Use suitable certified seed",
#                     "Maintain recommended sowing depth",
#                 ],
#             },
#             {
#                 "stage": "Vegetative Growth",
#                 "start_day": 16,
#                 "end_day": 55,
#                 "activities": [
#                     "Control weeds",
#                     "Monitor crop establishment",
#                 ],
#             },
#             {
#                 "stage": "Flowering and Grain Filling",
#                 "start_day": 56,
#                 "end_day": 95,
#                 "activities": [
#                     "Monitor irrigation requirements",
#                     "Monitor disease pressure",
#                 ],
#             },
#             {
#                 "stage": "Maturity and Harvest",
#                 "start_day": 96,
#                 "end_day": 120,
#                 "activities": [
#                     "Reduce irrigation near maturity",
#                     "Harvest at suitable grain moisture",
#                 ],
#             },
#         ],
#     },

#     "Potato": {
#         "temperature_min": 15,
#         "temperature_max": 25,
#         "rain_min": 20,
#         "rain_max": 80,
#         "season_months": [10, 11, 12, 1, 2],
#         "elevation_max": 2000,
#         "duration_days": 100,
#         "stages": [
#             {
#                 "stage": "Land Preparation",
#                 "start_day": 1,
#                 "end_day": 10,
#                 "activities": [
#                     "Prepare loose, well-drained soil",
#                     "Form suitable beds or ridges",
#                 ],
#             },
#             {
#                 "stage": "Planting",
#                 "start_day": 11,
#                 "end_day": 15,
#                 "activities": [
#                     "Plant healthy seed tubers",
#                     "Maintain recommended spacing",
#                 ],
#             },
#             {
#                 "stage": "Vegetative Growth",
#                 "start_day": 16,
#                 "end_day": 45,
#                 "activities": [
#                     "Control weeds",
#                     "Monitor soil moisture",
#                 ],
#             },
#             {
#                 "stage": "Tuber Development",
#                 "start_day": 46,
#                 "end_day": 80,
#                 "activities": [
#                     "Maintain suitable moisture",
#                     "Monitor late blight and pests",
#                 ],
#             },
#             {
#                 "stage": "Maturity and Harvest",
#                 "start_day": 81,
#                 "end_day": 100,
#                 "activities": [
#                     "Allow tubers to mature",
#                     "Harvest carefully to avoid damage",
#                 ],
#             },
#         ],
#     },

#     "Tomato": {
#         "temperature_min": 18,
#         "temperature_max": 30,
#         "rain_min": 20,
#         "rain_max": 100,
#         "season_months": [10, 11, 12, 1, 2],
#         "elevation_max": 1500,
#         "duration_days": 110,
#         "stages": [
#             {
#                 "stage": "Nursery / Land Preparation",
#                 "start_day": 1,
#                 "end_day": 15,
#                 "activities": [
#                     "Prepare healthy seedlings",
#                     "Prepare well-drained planting beds",
#                 ],
#             },
#             {
#                 "stage": "Transplanting",
#                 "start_day": 16,
#                 "end_day": 25,
#                 "activities": [
#                     "Transplant healthy seedlings",
#                     "Maintain suitable plant spacing",
#                 ],
#             },
#             {
#                 "stage": "Vegetative Growth",
#                 "start_day": 26,
#                 "end_day": 55,
#                 "activities": [
#                     "Control weeds",
#                     "Monitor nutrient requirements",
#                 ],
#             },
#             {
#                 "stage": "Flowering and Fruiting",
#                 "start_day": 56,
#                 "end_day": 90,
#                 "activities": [
#                     "Monitor pests and diseases",
#                     "Maintain consistent soil moisture",
#                 ],
#             },
#             {
#                 "stage": "Harvest",
#                 "start_day": 91,
#                 "end_day": 110,
#                 "activities": [
#                     "Harvest mature fruits regularly",
#                     "Handle fruits carefully",
#                 ],
#             },
#         ],
#     },
# }


# # ============================================================
# # LLM INITIALIZATION
# # ============================================================

# if not GROQ_API_KEY:
#     logger.warning(
#         "GROQ_API_KEY is not configured. "
#         "AI recommendation generation will fail until it is set."
#     )


# llm = (
#     ChatGroq(
#         api_key=GROQ_API_KEY,
#         model=GROQ_MODEL,
#         temperature=0.1,
#     )
#     if GROQ_API_KEY
#     else None
# )


# # ============================================================
# # PROMPT
# # ============================================================

# PROMPT = """
# You are an agricultural decision-support assistant for KrishiMap AI.

# You must reason ONLY from the supplied farm, weather, terrain,
# satellite, and deterministic crop-scoring data.

# IMPORTANT RULES:

# 1. Do not invent weather data.
# 2. Do not invent satellite observations.
# 3. Do not invent elevation.
# 4. Do not claim soil measurements that were not supplied.
# 5. NDVI, NDMI and BSI are remote-sensing indicators/proxies,
#    not direct laboratory soil or crop measurements.
# 6. Elevation is a terrain indicator.
# 7. Use the supplied seven-day weather forecast.
# 8. Do not modify the deterministic crop scores.
# 9. The deterministic ranking and scores are authoritative.
# 10. You may explain the scores but must not replace them.
# 11. Compare the current crop with the recommended crop when
#     a current crop is available.
# 12. Use the supplied crop schedule.
# 13. Respond in the requested language.
# 14. Return valid JSON only.
# 15. Do not wrap the JSON in markdown code fences.

# Requested language:
# {language}

# Farm context:
# {farm_context}

# Deterministic crop analysis:
# {deterministic_analysis}

# Return JSON with these fields:

# {{
#     "why_recommended": "string",
#     "farm_insights": ["string"],
#     "weather_risk": ["string"],
#     "satellite_insights": ["string"],
#     "terrain_insights": ["string"],
#     "farmer_advice": ["string"],
#     "explanation": "string"
# }}

# Do not add additional top-level fields.
# """


# prompt = ChatPromptTemplate.from_template(PROMPT)

# chain = (
#     prompt | llm
#     if llm is not None
#     else None
# )


# # ============================================================
# # NUMERIC HELPERS
# # ============================================================

# def clamp(
#     value: float,
#     minimum: float = 0.0,
#     maximum: float = 100.0,
# ) -> float:
#     return max(
#         minimum,
#         min(maximum, value),
#     )


# def average(values: list[float]) -> float:
#     if not values:
#         return 0.0

#     return sum(values) / len(values)


# # ============================================================
# # SCORE HELPERS
# # ============================================================

# def range_score(
#     value: float,
#     minimum: float,
#     maximum: float,
# ) -> float:
#     """
#     Score a value against a preferred range.

#     100 = inside the preferred range.
#     Score decreases as the value moves away from the range.
#     """

#     if minimum <= value <= maximum:
#         return 100.0

#     if value < minimum:
#         distance = minimum - value

#     else:
#         distance = value - maximum

#     range_width = max(
#         maximum - minimum,
#         1.0,
#     )

#     return clamp(
#         100.0 - (distance / range_width) * 100.0
#     )


# def rainfall_score(
#     rainfall: float,
#     minimum: float,
#     maximum: float,
# ) -> float:
#     """
#     Score total forecast rainfall against the crop's preferred
#     seven-day rainfall range.
#     """

#     return range_score(
#         rainfall,
#         minimum,
#         maximum,
#     )


# def season_score(
#     month: int,
#     season_months: list[int],
# ) -> float:
#     if month in season_months:
#         return 100.0

#     return 25.0


# def vegetation_score(
#     ndvi: float | None,
# ) -> float:
#     """
#     NDVI is treated as a vegetation-condition proxy.

#     Missing satellite data is intentionally neutral rather than
#     being interpreted as poor vegetation.
#     """

#     if ndvi is None:
#         return 50.0

#     try:
#         ndvi = float(ndvi)

#     except (TypeError, ValueError):
#         return 50.0

#     # Typical NDVI range is approximately -1 to +1.
#     normalized = ((ndvi + 1.0) / 2.0) * 100.0

#     return clamp(normalized)


# def elevation_score(
#     elevation: float | None,
#     maximum_elevation: float,
# ) -> float:
#     """
#     Score terrain suitability based on elevation.

#     Missing elevation is treated as neutral.
#     """

#     if elevation is None:
#         return 50.0

#     try:
#         elevation = float(elevation)

#     except (TypeError, ValueError):
#         return 50.0

#     if elevation <= maximum_elevation:
#         return 100.0

#     excess = elevation - maximum_elevation

#     # Gradual penalty rather than an abrupt zero.
#     return clamp(
#         100.0 - (excess / max(maximum_elevation, 1.0)) * 100.0
#     )


# # ============================================================
# # CROP SCORE
# # ============================================================

# def calculate_crop_score(
#     crop_name: str,
#     weather: dict[str, Any],
#     satellite: dict[str, Any],
#     elevation: float | None,
#     month: int,
# ) -> dict[str, Any]:
#     """
#     Calculate deterministic crop suitability.

#     These weights are intentionally preserved from the existing
#     implementation so the frontend's score behavior does not
#     unexpectedly change.
#     """

#     profile = CROP_PROFILES[crop_name]

#     current = weather.get(
#         "current",
#         {},
#     )

#     daily = weather.get(
#         "daily",
#         {},
#     )

#     # --------------------------------------------------------
#     # TEMPERATURE
#     # --------------------------------------------------------

#     max_temperatures = daily.get(
#         "temperature_2m_max",
#         [],
#     )

#     min_temperatures = daily.get(
#         "temperature_2m_min",
#         [],
#     )

#     if max_temperatures:
#         forecast_temperature = average(
#             [
#                 float(value)
#                 for value in max_temperatures
#                 if value is not None
#             ]
#         )

#     elif current.get("temperature_2m") is not None:
#         forecast_temperature = float(
#             current["temperature_2m"]
#         )

#     else:
#         forecast_temperature = (
#             profile["temperature_min"]
#             + profile["temperature_max"]
#         ) / 2.0

#     temperature_score = range_score(
#         forecast_temperature,
#         profile["temperature_min"],
#         profile["temperature_max"],
#     )

#     # --------------------------------------------------------
#     # RAINFALL
#     # --------------------------------------------------------

#     rain_values = daily.get(
#         "rain_sum",
#         [],
#     )

#     total_rainfall = sum(
#         float(value)
#         for value in rain_values
#         if value is not None
#     )

#     rainfall_component = rainfall_score(
#         total_rainfall,
#         profile["rain_min"],
#         profile["rain_max"],
#     )

#     # --------------------------------------------------------
#     # SEASON
#     # --------------------------------------------------------

#     season_component = season_score(
#         month,
#         profile["season_months"],
#     )

#     # --------------------------------------------------------
#     # SATELLITE / VEGETATION
#     # --------------------------------------------------------

#     ndvi = satellite.get("ndvi")

#     vegetation_component = vegetation_score(
#         ndvi
#     )

#     # --------------------------------------------------------
#     # TERRAIN
#     # --------------------------------------------------------

#     terrain_component = elevation_score(
#         elevation,
#         profile["elevation_max"],
#     )

#     # --------------------------------------------------------
#     # SOIL
#     # --------------------------------------------------------
#     #
#     # No direct soil data is currently supplied to the model.
#     # Keep this neutral rather than fabricating a soil score.
#     # --------------------------------------------------------

#     soil_component = 50.0

#     # --------------------------------------------------------
#     # FINAL WEIGHTED SCORE
#     # --------------------------------------------------------

#     score = (
#         rainfall_component * 0.25
#         + temperature_score * 0.30
#         + soil_component * 0.10
#         + season_component * 0.15
#         + vegetation_component * 0.15
#         + terrain_component * 0.05
#     )

#     return {
#         "crop": crop_name,
#         "score": round(
#             clamp(score),
#             2,
#         ),
#         "rainfall_score": round(
#             clamp(rainfall_component),
#             2,
#         ),
#         "temperature_score": round(
#             clamp(temperature_score),
#             2,
#         ),
#         "soil_score": round(
#             clamp(soil_component),
#             2,
#         ),
#         "season_score": round(
#             clamp(season_component),
#             2,
#         ),
#         "vegetation_score": round(
#             clamp(vegetation_component),
#             2,
#         ),
#         "terrain_score": round(
#             clamp(terrain_component),
#             2,
#         ),
#     }


# # ============================================================
# # DETERMINISTIC ANALYSIS
# # ============================================================

# def build_deterministic_analysis(
#     farm_context: dict[str, Any],
# ) -> dict[str, Any]:
#     """
#     Generate all deterministic crop scores before invoking the LLM.
#     """

#     weather = farm_context.get(
#         "weather",
#         {},
#     )

#     satellite = farm_context.get(
#         "satellite",
#         {},
#     )

#     terrain = farm_context.get(
#         "terrain",
#         {},
#     )

#     elevation = terrain.get(
#         "elevation"
#     )

#     month = datetime.now(
#         timezone.utc
#     ).month

#     crop_scores = []

#     for crop_name in CROP_PROFILES:
#         crop_score = calculate_crop_score(
#             crop_name=crop_name,
#             weather=weather,
#             satellite=satellite,
#             elevation=elevation,
#             month=month,
#         )

#         crop_scores.append(crop_score)

#     crop_scores.sort(
#         key=lambda item: item["score"],
#         reverse=True,
#     )

#     recommended_crop = crop_scores[0]["crop"]

#     current_crop = (
#         farm_context
#         .get("farm", {})
#         .get("current_crop")
#     )

#     return {
#         "recommended_crop": recommended_crop,
#         "current_crop": current_crop,
#         "scores": crop_scores,
#     }


# # ============================================================
# # SAFE JSON PARSING
# # ============================================================

# def parse_llm_json(
#     content: Any,
# ) -> dict[str, Any]:
#     """
#     Parse JSON returned by Groq.

#     Handles common cases where the model returns markdown
#     code fences despite being instructed not to.
#     """

#     if content is None:
#         raise ValueError(
#             "LLM returned an empty response."
#         )

#     if isinstance(content, list):
#         # Some LangChain versions may return structured content.
#         parts = []

#         for item in content:
#             if isinstance(item, str):
#                 parts.append(item)

#             elif isinstance(item, dict):
#                 text = item.get("text")

#                 if text:
#                     parts.append(str(text))

#         content = "".join(parts)

#     content = str(content).strip()

#     if content.startswith("```"):
#         lines = content.splitlines()

#         if lines:
#             lines = lines[1:]

#         if lines and lines[-1].strip() == "```":
#             lines = lines[:-1]

#         content = "\n".join(lines).strip()

#     try:
#         parsed = json.loads(content)

#     except json.JSONDecodeError as exc:
#         logger.error(
#             "Groq returned invalid JSON: %s",
#             content[:1000],
#         )

#         raise ValueError(
#             "AI service returned invalid recommendation data."
#         ) from exc

#     if not isinstance(parsed, dict):
#         raise ValueError(
#             "AI recommendation must be a JSON object."
#         )

#     return parsed


# # ============================================================
# # NORMALIZATION HELPERS
# # ============================================================

# def ensure_string_list(
#     value: Any,
# ) -> list[str]:
#     if value is None:
#         return []

#     if isinstance(value, str):
#         return [value]

#     if not isinstance(value, list):
#         return []

#     return [
#         str(item)
#         for item in value
#         if item is not None
#     ]


# def safe_string(
#     value: Any,
#     default: str = "",
# ) -> str:
#     if value is None:
#         return default

#     return str(value)


# # ============================================================
# # AI FALLBACK
# # ============================================================

# def build_fallback_ai_response(
#     recommended_crop: str,
#     current_crop: str | None,
# ) -> dict[str, Any]:
#     """
#     Safe fallback when Groq is unavailable.

#     This allows the deterministic recommendation system to remain
#     useful even when the optional AI explanation service is down.
#     """

#     if current_crop:
#         explanation = (
#             f"{recommended_crop} received the highest deterministic "
#             f"suitability score from the available farm, weather, "
#             f"terrain and satellite inputs. The current crop is "
#             f"{current_crop}."
#         )
#     else:
#         explanation = (
#             f"{recommended_crop} received the highest deterministic "
#             f"suitability score from the available farm, weather, "
#             f"terrain and satellite inputs."
#         )

#     return {
#         "why_recommended": explanation,
#         "farm_insights": [
#             "Recommendation is based on the currently available farm data."
#         ],
#         "weather_risk": [
#             "Weather risk should be monitored using the latest forecast."
#         ],
#         "satellite_insights": [
#             "Satellite indicators are used when available."
#         ],
#         "terrain_insights": [
#             "Terrain suitability is evaluated using the available elevation data."
#         ],
#         "farmer_advice": [
#             "Verify local field conditions before making planting decisions."
#         ],
#         "explanation": explanation,
#     }


# # ============================================================
# # MAIN RECOMMENDATION FUNCTION
# # ============================================================

# def get_crop_recommendation(
#     farm_context: dict[str, Any],
#     language: str = "en",
# ) -> dict[str, Any]:
#     """
#     Generate a crop recommendation.

#     This function intentionally remains synchronous because the
#     router executes it using FastAPI's run_in_threadpool().

#     Keeping the deterministic calculation and Groq call together
#     preserves the existing service interface.
#     """

#     language = language.lower().strip()

#     if language not in SUPPORTED_LANGUAGES:
#         raise ValueError(
#             f"Unsupported language: {language}"
#         )

#     # ========================================================
#     # DETERMINISTIC ANALYSIS
#     # ========================================================

#     deterministic = build_deterministic_analysis(
#         farm_context
#     )

#     recommended_crop = deterministic[
#         "recommended_crop"
#     ]

#     current_crop = deterministic.get(
#         "current_crop"
#     )

#     scores = deterministic[
#         "scores"
#     ]

#     # ========================================================
#     # COMPARE CURRENT CROP
#     # ========================================================

#     current_crop_data = None

#     if current_crop:
#         for item in scores:
#             if item["crop"].lower() == str(
#                 current_crop
#             ).lower():
#                 current_crop_data = item
#                 break

#     recommended_crop_data = next(
#         (
#             item
#             for item in scores
#             if item["crop"] == recommended_crop
#         ),
#         None,
#     )

#     # ========================================================
#     # BUILD AI CONTEXT
#     # ========================================================

#     ai_input = {
#         "farm": farm_context.get(
#             "farm",
#             {},
#         ),
#         "farmer": farm_context.get(
#             "farmer",
#             {},
#         ),
#         "weather": farm_context.get(
#             "weather",
#             {},
#         ),
#         "satellite": farm_context.get(
#             "satellite",
#             {},
#         ),
#         "terrain": farm_context.get(
#             "terrain",
#             {},
#         ),
#     }

#     # Keep the prompt compact enough to reduce unnecessary
#     # token usage.
#     deterministic_prompt_data = {
#         "recommended_crop": recommended_crop,
#         "current_crop": current_crop,
#         "crop_scores": scores,
#     }

#     # ========================================================
#     # DEFAULT AI RESPONSE
#     # ========================================================

#     ai_response = build_fallback_ai_response(
#         recommended_crop,
#         current_crop,
#     )

#     # ========================================================
#     # GROQ
#     # ========================================================

#     if chain is not None:

#         try:
#             response = chain.invoke(
#                 {
#                     "language": language,
#                     "farm_context": json.dumps(
#                         ai_input,
#                         ensure_ascii=False,
#                         separators=(",", ":"),
#                     ),
#                     "deterministic_analysis": json.dumps(
#                         deterministic_prompt_data,
#                         ensure_ascii=False,
#                         separators=(",", ":"),
#                     ),
#                 }
#             )

#             content = getattr(
#                 response,
#                 "content",
#                 response,
#             )

#             parsed = parse_llm_json(
#                 content
#             )

#             ai_response = {
#                 "why_recommended": safe_string(
#                     parsed.get(
#                         "why_recommended"
#                     ),
#                     ai_response["why_recommended"],
#                 ),
#                 "farm_insights": ensure_string_list(
#                     parsed.get(
#                         "farm_insights"
#                     )
#                 ),
#                 "weather_risk": ensure_string_list(
#                     parsed.get(
#                         "weather_risk"
#                     )
#                 ),
#                 "satellite_insights": ensure_string_list(
#                     parsed.get(
#                         "satellite_insights"
#                     )
#                 ),
#                 "terrain_insights": ensure_string_list(
#                     parsed.get(
#                         "terrain_insights"
#                     )
#                 ),
#                 "farmer_advice": ensure_string_list(
#                     parsed.get(
#                         "farmer_advice"
#                     )
#                 ),
#                 "explanation": safe_string(
#                     parsed.get(
#                         "explanation"
#                     ),
#                     ai_response["explanation"],
#                 ),
#             }

#             # Prevent an incomplete LLM response from producing
#             # empty user-facing sections.
#             if not ai_response["farm_insights"]:
#                 ai_response["farm_insights"] = (
#                     [
#                         "Recommendation is based on the available "
#                         "farm and environmental data."
#                     ]
#                 )

#             if not ai_response["weather_risk"]:
#                 ai_response["weather_risk"] = (
#                     [
#                         "Monitor the latest local weather forecast "
#                         "during crop establishment and growth."
#                     ]
#                 )

#             if not ai_response["satellite_insights"]:
#                 ai_response["satellite_insights"] = (
#                     [
#                         "Satellite indicators are included when available."
#                     ]
#                 )

#             if not ai_response["terrain_insights"]:
#                 ai_response["terrain_insights"] = (
#                     [
#                         "Terrain suitability is evaluated from "
#                         "available elevation information."
#                     ]
#                 )

#             if not ai_response["farmer_advice"]:
#                 ai_response["farmer_advice"] = (
#                     [
#                         "Verify local field conditions before "
#                         "making final crop decisions."
#                     ]
#                 )

#         except Exception:
#             logger.exception(
#                 "Groq recommendation generation failed. "
#                 "Using deterministic fallback."
#             )

#     else:
#         logger.warning(
#             "Groq chain is unavailable. "
#             "Using deterministic fallback."
#         )

#     # ========================================================
#     # COMPARISON
#     # ========================================================

#     comparison = {
#         "current_crop": current_crop,
#         "recommended_crop": recommended_crop,
#         "current_crop_score": (
#             current_crop_data["score"]
#             if current_crop_data
#             else None
#         ),
#         "recommended_crop_score": (
#             recommended_crop_data["score"]
#             if recommended_crop_data
#             else None
#         ),
#         "reason": ai_response[
#             "why_recommended"
#         ],
#     }

#     # ========================================================
#     # SCHEDULE
#     # ========================================================

#     recommended_profile = CROP_PROFILES[
#         recommended_crop
#     ]

#     schedule = {
#         "crop": recommended_crop,
#         "duration_days": recommended_profile[
#             "duration_days"
#         ],
#         "stages": recommended_profile[
#             "stages"
#         ],
#     }

#     # ========================================================
#     # INSIGHT DATA
#     # ========================================================

#     satellite = farm_context.get(
#         "satellite",
#         {},
#     )

#     terrain = farm_context.get(
#         "terrain",
#         {},
#     )

#     weather = farm_context.get(
#         "weather",
#         {},
#     )

#     # ========================================================
#     # FINAL RESPONSE
#     # ========================================================
#     #
#     # IMPORTANT:
#     #
#     # These fields preserve the existing frontend-facing
#     # recommendation contract.
#     # ========================================================

#     final_response = {
#         # ----------------------------------------------------
#         # Primary recommendation
#         # ----------------------------------------------------

#         "language": language,

#         "intended_crop": current_crop,

#         "recommended_crop": recommended_crop,

#         "recommendation_score": (
#             recommended_crop_data["score"]
#             if recommended_crop_data
#             else 0.0
#         ),

#         # ----------------------------------------------------
#         # AI explanation
#         # ----------------------------------------------------

#         "why_recommended": ai_response[
#             "why_recommended"
#         ],

#         "comparison": comparison,

#         "farm_insights": ai_response[
#             "farm_insights"
#         ],

#         "weather_risk": ai_response[
#             "weather_risk"
#         ],

#         "satellite_insights": ai_response[
#             "satellite_insights"
#         ],

#         "terrain_insights": ai_response[
#             "terrain_insights"
#         ],

#         "schedule": schedule,

#         "farmer_advice": ai_response[
#             "farmer_advice"
#         ],

#         "explanation": ai_response[
#             "explanation"
#         ],

#         # ----------------------------------------------------
#         # Backward-compatible fields
#         # ----------------------------------------------------

#         "crop": recommended_crop,

#         "suitability_score": (
#             recommended_crop_data["score"]
#             if recommended_crop_data
#             else 0.0
#         ),

#         "rainfall_score": (
#             recommended_crop_data[
#                 "rainfall_score"
#             ]
#             if recommended_crop_data
#             else 0.0
#         ),

#         "temperature_score": (
#             recommended_crop_data[
#                 "temperature_score"
#             ]
#             if recommended_crop_data
#             else 0.0
#         ),

#         "soil_score": (
#             recommended_crop_data[
#                 "soil_score"
#             ]
#             if recommended_crop_data
#             else 50.0
#         ),

#         "season_score": (
#             recommended_crop_data[
#                 "season_score"
#             ]
#             if recommended_crop_data
#             else 0.0
#         ),

#         "vegetation_score": (
#             recommended_crop_data[
#                 "vegetation_score"
#             ]
#             if recommended_crop_data
#             else 50.0
#         ),

#         # ----------------------------------------------------
#         # Supporting data
#         # ----------------------------------------------------

#         "satellite": satellite,

#         "terrain": terrain,

#         "forecast": weather.get(
#             "daily",
#             {},
#         ),
#     }

#     return final_response
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("krishimap.recommendation")


# ============================================================================
# CROP PROFILES
# ============================================================================

CROP_PROFILES: dict[str, dict[str, Any]] = {
    "Rice": {
        "rainfall": (1000, 2000),
        "temperature": (20, 35),
        "soil": [
            "clay",
            "clay loam",
            "loam",
        ],
        "seasons": [
            "kharif",
            "monsoon",
        ],
        "stages": [
            "land preparation",
            "nursery/transplanting",
            "vegetative growth",
            "panicle initiation",
            "flowering",
            "grain filling",
            "harvesting",
        ],
    },
    "Maize": {
        "rainfall": (500, 1200),
        "temperature": (18, 32),
        "soil": [
            "loam",
            "sandy loam",
            "clay loam",
        ],
        "seasons": [
            "kharif",
            "rabi",
            "summer",
        ],
        "stages": [
            "land preparation",
            "sowing",
            "vegetative growth",
            "tasseling",
            "silking",
            "grain filling",
            "harvesting",
        ],
    },
    "Wheat": {
        "rainfall": (300, 900),
        "temperature": (10, 25),
        "soil": [
            "loam",
            "clay loam",
            "silt loam",
        ],
        "seasons": [
            "rabi",
            "winter",
        ],
        "stages": [
            "land preparation",
            "sowing",
            "crown root initiation",
            "tillering",
            "jointing",
            "flowering",
            "grain filling",
            "harvesting",
        ],
    },
    "Potato": {
        "rainfall": (500, 750),
        "temperature": (15, 25),
        "soil": [
            "sandy loam",
            "loam",
        ],
        "seasons": [
            "rabi",
            "winter",
        ],
        "stages": [
            "land preparation",
            "planting",
            "vegetative growth",
            "tuber initiation",
            "tuber bulking",
            "maturation",
            "harvesting",
        ],
    },
    "Tomato": {
        "rainfall": (400, 800),
        "temperature": (18, 30),
        "soil": [
            "loam",
            "sandy loam",
            "clay loam",
        ],
        "seasons": [
            "rabi",
            "kharif",
            "summer",
        ],
        "stages": [
            "nursery",
            "transplanting",
            "vegetative growth",
            "flowering",
            "fruit setting",
            "fruit development",
            "harvesting",
        ],
    },
}


# ============================================================================
# SCORING WEIGHTS
# ============================================================================

SCORING_WEIGHTS = {
    "rainfall": 0.25,
    "temperature": 0.30,
    "soil": 0.10,
    "season": 0.15,
    "vegetation": 0.15,
    "terrain": 0.05,
}


# ============================================================================
# GROQ CONFIGURATION
# ============================================================================

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

_llm = None
_chain = None


def _initialize_llm() -> None:
    """
    Lazily initialize the Groq/LangChain pipeline.

    Lazy initialization avoids loading the AI stack during application
    startup when recommendations are not being requested.
    """

    global _llm
    global _chain

    if _chain is not None:
        return

    if not GROQ_API_KEY:
        logger.warning(
            "GROQ_API_KEY is not configured. "
            "AI recommendation enhancement is disabled."
        )
        return

    try:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import PromptTemplate
        from langchain_groq import ChatGroq

        _llm = ChatGroq(
            model=GROQ_MODEL,
            api_key=GROQ_API_KEY,
            temperature=0.2,
        )

        prompt = PromptTemplate.from_template(
            """
You are an agricultural recommendation assistant.

Analyze the supplied farm information and deterministic crop scores.

Return ONLY valid JSON.

Required JSON structure:

{{
    "why_recommended": "short explanation",
    "farm_insights": ["insight 1", "insight 2"],
    "weather_risk": "short weather risk assessment",
    "satellite_insights": ["insight 1"],
    "terrain_insights": ["insight 1"],
    "farmer_advice": ["advice 1", "advice 2"],
    "explanation": "short overall explanation"
}}

Farm information:
{farm_context}

Selected crop:
{recommended_crop}

Deterministic scores:
{scores}

Language:
{language}
"""
        )

        _chain = prompt | _llm | StrOutputParser()

        logger.info(
            "Groq recommendation pipeline initialized with model=%s",
            GROQ_MODEL,
        )

    except Exception:
        logger.exception(
            "Failed to initialize Groq recommendation pipeline."
        )

        _llm = None
        _chain = None


# ============================================================================
# NUMERIC HELPERS
# ============================================================================

def _safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    try:
        if value is None:
            return default

        return float(value)

    except (TypeError, ValueError):
        return default


def _clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    return max(
        minimum,
        min(maximum, value),
    )


def _range_score(
    value: float | None,
    target_range: tuple[float, float],
) -> float:
    """
    Score a value against an ideal range.

    100 = inside the target range.
    Score decreases smoothly as the value moves away from the range.
    """

    if value is None:
        return 50.0

    value = _safe_float(value)

    minimum, maximum = target_range

    if minimum <= value <= maximum:
        return 100.0

    if value < minimum:
        distance = minimum - value
    else:
        distance = value - maximum

    span = max(
        maximum - minimum,
        1.0,
    )

    return _clamp(
        100.0 - (distance / span) * 100.0
    )


# ============================================================================
# SEASON DETECTION
# ============================================================================

def _current_season() -> str:
    """
    Determine a broad agricultural season from the current UTC month.

    The deterministic model is intentionally simple and can later be
    replaced by region-specific agricultural calendars.
    """

    month = datetime.now(timezone.utc).month

    if month in (6, 7, 8, 9, 10):
        return "kharif"

    if month in (11, 12, 1, 2):
        return "rabi"

    return "summer"


# ============================================================================
# DETERMINISTIC SCORING
# ============================================================================

def _calculate_crop_score(
    crop: str,
    farm_context: dict[str, Any],
) -> dict[str, float]:
    profile = CROP_PROFILES[crop]

    weather = farm_context.get("weather") or {}
    current = weather.get("current") or {}

    rainfall = _safe_float(
        current.get("precipitation"),
        default=None,
    )

    temperature = _safe_float(
        current.get("temperature_2m"),
        default=None,
    )

    soil_type = str(
        farm_context.get("soil_type") or ""
    ).lower()

    season = _current_season()

    # ------------------------------------------------------------------------
    # Rainfall
    # ------------------------------------------------------------------------

    rainfall_score = _range_score(
        rainfall,
        profile["rainfall"],
    )

    # ------------------------------------------------------------------------
    # Temperature
    # ------------------------------------------------------------------------

    temperature_score = _range_score(
        temperature,
        profile["temperature"],
    )

    # ------------------------------------------------------------------------
    # Soil
    # ------------------------------------------------------------------------

    soil_score = 50.0

    if soil_type:
        soil_score = (
            100.0
            if any(
                expected in soil_type
                for expected in profile["soil"]
            )
            else 30.0
        )

    # ------------------------------------------------------------------------
    # Season
    # ------------------------------------------------------------------------

    season_score = (
        100.0
        if season in profile["seasons"]
        else 30.0
    )

    # ------------------------------------------------------------------------
    # Vegetation
    # ------------------------------------------------------------------------

    satellite = farm_context.get("satellite") or {}

    ndvi = satellite.get("ndvi")

    if ndvi is None:
        vegetation_score = 50.0
    else:
        ndvi = _safe_float(ndvi)

        # Generic vegetation suitability.
        vegetation_score = _clamp(
            ndvi * 100.0
        )

    # ------------------------------------------------------------------------
    # Terrain
    # ------------------------------------------------------------------------

    terrain = farm_context.get("terrain") or {}

    slope = terrain.get("slope")

    if slope is None:
        terrain_score = 50.0
    else:
        slope = _safe_float(slope)

        if slope <= 3:
            terrain_score = 100.0
        elif slope <= 8:
            terrain_score = 75.0
        elif slope <= 15:
            terrain_score = 50.0
        else:
            terrain_score = 25.0

    return {
        "rainfall_score": round(
            rainfall_score,
            2,
        ),
        "temperature_score": round(
            temperature_score,
            2,
        ),
        "soil_score": round(
            soil_score,
            2,
        ),
        "season_score": round(
            season_score,
            2,
        ),
        "vegetation_score": round(
            vegetation_score,
            2,
        ),
        "terrain_score": round(
            terrain_score,
            2,
        ),
    }


def _calculate_total_score(
    scores: dict[str, float],
) -> float:
    """
    Calculate the weighted deterministic suitability score.
    """

    total = (
        scores["rainfall_score"]
        * SCORING_WEIGHTS["rainfall"]
        + scores["temperature_score"]
        * SCORING_WEIGHTS["temperature"]
        + scores["soil_score"]
        * SCORING_WEIGHTS["soil"]
        + scores["season_score"]
        * SCORING_WEIGHTS["season"]
        + scores["vegetation_score"]
        * SCORING_WEIGHTS["vegetation"]
        + scores["terrain_score"]
        * SCORING_WEIGHTS["terrain"]
    )

    return round(
        _clamp(total),
        2,
    )


# ============================================================================
# AI RESPONSE PARSING
# ============================================================================

def _parse_ai_response(
    raw_response: str,
) -> dict[str, Any]:
    """
    Safely parse the LLM response.

    Handles:
        - plain JSON
        - markdown ```json blocks
        - accidental surrounding text
    """

    if not raw_response:
        return {}

    text = raw_response.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    try:
        parsed = json.loads(text)

        if isinstance(parsed, dict):
            return parsed

    except json.JSONDecodeError:
        pass

    # Attempt to extract the first JSON object.
    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:
        try:
            parsed = json.loads(
                text[start : end + 1]
            )

            if isinstance(parsed, dict):
                return parsed

        except json.JSONDecodeError:
            pass

    logger.warning(
        "Groq returned a response that could not be parsed as JSON."
    )

    return {}


# ============================================================================
# FALLBACK CONTENT
# ============================================================================

def _fallback_ai_content(
    recommended_crop: str,
    scores: dict[str, float],
    language: str,
) -> dict[str, Any]:
    """
    Deterministic fallback used when Groq is unavailable.

    This allows the recommendation API to remain operational even when
    the external AI service is down.
    """

    score = scores["total_score"]

    if language == "hi":
        return {
            "why_recommended": (
                f"{recommended_crop} का वर्तमान खेत और मौसम "
                f"परिस्थितियों के आधार पर उपयुक्तता स्कोर "
                f"{score:.1f}% है।"
            ),
            "farm_insights": [
                "मौसम और खेत की स्थिति की नियमित निगरानी करें।",
                "सिंचाई और मिट्टी की नमी को फसल के चरण के अनुसार बनाए रखें।",
            ],
            "weather_risk": (
                "स्थानीय मौसम पूर्वानुमान की नियमित जांच करें।"
            ),
            "satellite_insights": [
                "वर्तमान में उपग्रह संकेतक उपलब्ध नहीं हैं।"
            ],
            "terrain_insights": [
                "वर्तमान में विस्तृत भू-भाग संकेतक उपलब्ध नहीं हैं।"
            ],
            "farmer_advice": [
                "बुवाई और सिंचाई का निर्णय स्थानीय परिस्थितियों के अनुसार लें।",
                "फसल की वृद्धि के दौरान नियमित निरीक्षण करें।",
            ],
            "explanation": (
                "यह सुझाव उपलब्ध खेत, मौसम और "
                "दृढ़निश्चयी स्कोरिंग संकेतकों पर आधारित है।"
            ),
        }

    if language == "bn":
        return {
            "why_recommended": (
                f"বর্তমান জমি ও আবহাওয়ার তথ্য অনুযায়ী "
                f"{recommended_crop}-এর উপযুক্ততা স্কোর "
                f"{score:.1f}%।"
            ),
            "farm_insights": [
                "আবহাওয়া ও জমির অবস্থা নিয়মিত পর্যবেক্ষণ করুন।",
                "ফসলের পর্যায় অনুযায়ী সেচ ও মাটির আর্দ্রতা বজায় রাখুন।",
            ],
            "weather_risk": (
                "স্থানীয় আবহাওয়ার পূর্বাভাস নিয়মিত পরীক্ষা করুন।"
            ),
            "satellite_insights": [
                "বর্তমানে স্যাটেলাইট সূচক উপলব্ধ নেই।"
            ],
            "terrain_insights": [
                "বর্তমানে বিস্তারিত ভূখণ্ড সূচক উপলব্ধ নেই।"
            ],
            "farmer_advice": [
                "স্থানীয় পরিস্থিতি অনুযায়ী বপন ও সেচের সিদ্ধান্ত নিন।",
                "ফসলের বৃদ্ধি নিয়মিত পর্যবেক্ষণ করুন।",
            ],
            "explanation": (
                "এই সুপারিশ উপলব্ধ জমি, আবহাওয়া এবং "
                "নির্ধারিত স্কোরিং সূচকের উপর ভিত্তি করে তৈরি।"
            ),
        }

    return {
        "why_recommended": (
            f"{recommended_crop} has a suitability score of "
            f"{score:.1f}% based on the available farm and "
            "weather conditions."
        ),
        "farm_insights": [
            "Monitor field conditions regularly.",
            "Maintain soil moisture according to the crop growth stage.",
        ],
        "weather_risk": (
            "Monitor the local weather forecast regularly."
        ),
        "satellite_insights": [
            "Satellite indicators are currently unavailable."
        ],
        "terrain_insights": [
            "Detailed terrain indicators are currently unavailable."
        ],
        "farmer_advice": [
            "Adjust irrigation and sowing decisions to local conditions.",
            "Inspect crop growth regularly throughout the season.",
        ],
        "explanation": (
            "This recommendation is based on the available farm, "
            "weather, and deterministic scoring indicators."
        ),
    }


# ============================================================================
# SCHEDULE
# ============================================================================

def _build_schedule(
    crop: str,
) -> list[dict[str, Any]]:
    stages = CROP_PROFILES[crop]["stages"]

    schedule: list[dict[str, Any]] = []

    for index, stage in enumerate(stages, start=1):
        schedule.append(
            {
                "stage": stage,
                "step": index,
            }
        )

    return schedule


# ============================================================================
# MAIN RECOMMENDATION FUNCTION
# ============================================================================

def get_crop_recommendation(
    farm_context: dict[str, Any],
    language: str = "en",
) -> dict[str, Any]:
    """
    Generate a crop recommendation.

    This function intentionally remains synchronous because the router
    executes it in FastAPI's threadpool. This prevents synchronous LangChain
    / Groq work from blocking the event loop.
    """

    if language not in {"en", "hi", "bn"}:
        language = "en"

    # ------------------------------------------------------------------------
    # Calculate deterministic score for every supported crop.
    # ------------------------------------------------------------------------

    crop_scores: dict[str, dict[str, float]] = {}

    for crop in CROP_PROFILES:
        scores = _calculate_crop_score(
            crop,
            farm_context,
        )

        scores["total_score"] = _calculate_total_score(
            scores
        )

        crop_scores[crop] = scores

    # ------------------------------------------------------------------------
    # Select highest deterministic score.
    # ------------------------------------------------------------------------

    recommended_crop = max(
        crop_scores,
        key=lambda crop: crop_scores[crop]["total_score"],
    )

    selected_scores = crop_scores[
        recommended_crop
    ]

    recommendation_score = selected_scores[
        "total_score"
    ]

    # ------------------------------------------------------------------------
    # Intended crop from the farm, if supplied.
    # ------------------------------------------------------------------------

    intended_crop = farm_context.get(
        "crop"
    )

    if intended_crop:
        intended_crop = str(
            intended_crop
        ).strip()

    # ------------------------------------------------------------------------
    # Comparison data.
    # ------------------------------------------------------------------------

    comparison = []

    for crop, scores in sorted(
        crop_scores.items(),
        key=lambda item: item[1]["total_score"],
        reverse=True,
    ):
        comparison.append(
            {
                "crop": crop,
                "score": scores["total_score"],
                "reason": (
                    "Weighted suitability score based on "
                    "rainfall, temperature, soil, season, "
                    "vegetation, and terrain."
                ),
            }
        )

    # ------------------------------------------------------------------------
    # AI enhancement.
    # ------------------------------------------------------------------------

    ai_content: dict[str, Any] = {}

    _initialize_llm()

    if _chain is not None:
        try:
            raw_response = _chain.invoke(
                {
                    "farm_context": json.dumps(
                        farm_context,
                        default=str,
                        ensure_ascii=False,
                    ),
                    "recommended_crop": recommended_crop,
                    "scores": json.dumps(
                        selected_scores,
                        ensure_ascii=False,
                    ),
                    "language": language,
                }
            )

            ai_content = _parse_ai_response(
                raw_response
            )

        except Exception:
            logger.exception(
                "Groq recommendation generation failed. "
                "Using deterministic fallback."
            )

    if not ai_content:
        ai_content = _fallback_ai_content(
            recommended_crop=recommended_crop,
            scores=selected_scores,
            language=language,
        )

    # ------------------------------------------------------------------------
    # Ensure frontend-facing collections always have stable types.
    # ------------------------------------------------------------------------

    farm_insights = ai_content.get(
        "farm_insights",
        [],
    )

    if not isinstance(farm_insights, list):
        farm_insights = [str(farm_insights)]

    satellite_insights = ai_content.get(
        "satellite_insights",
        [],
    )

    if not isinstance(satellite_insights, list):
        satellite_insights = [str(satellite_insights)]

    terrain_insights = ai_content.get(
        "terrain_insights",
        [],
    )

    if not isinstance(terrain_insights, list):
        terrain_insights = [str(terrain_insights)]

    farmer_advice = ai_content.get(
        "farmer_advice",
        [],
    )

    if not isinstance(farmer_advice, list):
        farmer_advice = [str(farmer_advice)]

    # ------------------------------------------------------------------------
    # Final response.
    # ------------------------------------------------------------------------

    return {
        # Current frontend contract
        "language": language,
        "intended_crop": intended_crop,
        "recommended_crop": recommended_crop,
        "recommendation_score": recommendation_score,
        "why_recommended": ai_content.get(
            "why_recommended",
            "",
        ),
        "comparison": comparison,
        "farm_insights": farm_insights,
        "weather_risk": ai_content.get(
            "weather_risk",
            None,
        ),
        "satellite_insights": satellite_insights,
        "terrain_insights": terrain_insights,
        "schedule": _build_schedule(
            recommended_crop
        ),
        "farmer_advice": farmer_advice,
        "explanation": ai_content.get(
            "explanation",
            None,
        ),

        # Backward compatibility
        "crop": recommended_crop,
        "suitability_score": recommendation_score,
        "rainfall_score": selected_scores[
            "rainfall_score"
        ],
        "temperature_score": selected_scores[
            "temperature_score"
        ],
        "soil_score": selected_scores[
            "soil_score"
        ],
        "season_score": selected_scores[
            "season_score"
        ],
        "vegetation_score": selected_scores[
            "vegetation_score"
        ],

        # Raw supporting data
        "satellite": farm_context.get(
            "satellite"
        ),
        "terrain": farm_context.get(
            "terrain"
        ),
        "forecast": farm_context.get(
            "weather"
        ),
    }