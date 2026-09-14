
import { api } from "@/lib/api";

import {
  CropRecommendation,
  RecommendationLanguage,
} from "@/types/crop";


// =========================================================
// BACKEND TYPES
// =========================================================

interface BackendCropComparison {
  crop: string;
  score: number;
  reason: string;
}


interface BackendCropScheduleStage {
  stage: string;
  start_day: number;
  end_day: number;
  activities: string[];
}


interface BackendSatelliteInsights {
  available?: boolean;

  source?: string;

  acquisition_window_days?: number | null;

  ndvi?: number | null;

  ndmi?: number | null;

  bsi?: number | null;

  cloud_masked?: boolean;
}


interface BackendTopography {
  elevation_m?: number | null;

  source?: string;

  interpretation?: string;
}


interface BackendForecastInsight {
  date: string;

  temperature_max?: number | null;

  temperature_min?: number | null;

  rainfall?: number | null;

  precipitation_probability?: number | null;

  weather_code?: number | null;
}


interface BackendCropRecommendation {
  language?: RecommendationLanguage;

  intended_crop?: string | null;

  recommended_crop?: string;

  recommendation_score?: number;

  // -------------------------------------------------------
  // Existing component compatibility
  // -------------------------------------------------------

  crop?: string;

  suitability_score?: number;

  rainfall_score?: number;

  temperature_score?: number;

  soil_score?: number;

  season_score?: number;

  vegetation_score?: number;

  // -------------------------------------------------------
  // AI explanation
  // -------------------------------------------------------

  why_recommended?: string;

  explanation?: string;

  // -------------------------------------------------------
  // Comparison
  // -------------------------------------------------------

  comparison?: BackendCropComparison[];

  // -------------------------------------------------------
  // Insights
  // -------------------------------------------------------

  farm_insights?: string[];

  weather_risk?: string[];

  satellite_insights?: string[];

  terrain_insights?: string[];

  // -------------------------------------------------------
  // Crop lifecycle
  // -------------------------------------------------------

  schedule?: BackendCropScheduleStage[];

  farmer_advice?: string[];

  // -------------------------------------------------------
  // Satellite
  // -------------------------------------------------------

  satellite_available?: boolean;

  satellite?: BackendSatelliteInsights | null;

  // -------------------------------------------------------
  // Terrain
  // -------------------------------------------------------

  topography?: BackendTopography;

  // -------------------------------------------------------
  // Forecast
  // -------------------------------------------------------

  seven_day_forecast?: BackendForecastInsight[];
}


// =========================================================
// HELPERS
// =========================================================

function toNumber(
  value: number | null | undefined,
  fallback = 0
): number {
  if (
    value === null ||
    value === undefined ||
    Number.isNaN(Number(value))
  ) {
    return fallback;
  }

  return Number(value);
}


function toNullableNumber(
  value: number | null | undefined
): number | null {
  if (
    value === null ||
    value === undefined ||
    Number.isNaN(Number(value))
  ) {
    return null;
  }

  return Number(value);
}


// =========================================================
// NORMALIZER
// =========================================================

function normalizeCropRecommendation(
  data: BackendCropRecommendation,
  language: RecommendationLanguage
): CropRecommendation {

  const recommendedCrop =
    data.recommended_crop ??
    data.crop ??
    "Unknown";


  const recommendationScore =
    toNumber(
      data.recommendation_score ??
        data.suitability_score,
      0
    );


  // =======================================================
  // Satellite
  // =======================================================

  const satellite =
    data.satellite
      ? {
          available:
            Boolean(
              data.satellite.available
            ),

          source:
            data.satellite.source,

          acquisitionWindowDays:
            data.satellite
              .acquisition_window_days ??
            null,

          ndvi:
            toNullableNumber(
              data.satellite.ndvi
            ),

          ndmi:
            toNullableNumber(
              data.satellite.ndmi
            ),

          bsi:
            toNullableNumber(
              data.satellite.bsi
            ),

          cloudMasked:
            Boolean(
              data.satellite
                .cloud_masked ??
                true
            ),
        }
      : null;


  // =======================================================
  // Topography
  // =======================================================

  const topography = {
    elevationM:
      toNullableNumber(
        data.topography
          ?.elevation_m
      ),

    source:
      data.topography?.source,

    interpretation:
      data.topography
        ?.interpretation,
  };


  // =======================================================
  // Forecast
  // =======================================================

  const sevenDayForecast =
    (
      data.seven_day_forecast ??
      []
    ).map((day) => ({
      date:
        day.date,

      temperatureMax:
        toNullableNumber(
          day.temperature_max
        ),

      temperatureMin:
        toNullableNumber(
          day.temperature_min
        ),

      rainfall:
        toNullableNumber(
          day.rainfall
        ),

      precipitationProbability:
        toNullableNumber(
          day.precipitation_probability
        ),

      weatherCode:
        day.weather_code ??
        null,
    }));


  // =======================================================
  // Final normalized frontend object
  // =======================================================

  return {
    // -----------------------------------------------------
    // Language
    // -----------------------------------------------------

    language:
      data.language ??
      language,


    // -----------------------------------------------------
    // Intended/current crop
    // -----------------------------------------------------

    intendedCrop:
      data.intended_crop ??
      null,


    // -----------------------------------------------------
    // Recommendation
    // -----------------------------------------------------

    recommendedCrop:
      recommendedCrop,

    recommendationScore:
      recommendationScore,


    // -----------------------------------------------------
    // Existing component compatibility
    // -----------------------------------------------------

    crop:
      recommendedCrop,

    suitabilityScore:
      recommendationScore,


    // -----------------------------------------------------
    // Score breakdown
    // -----------------------------------------------------

    rainfallScore:
      toNumber(
        data.rainfall_score,
        0
      ),

    temperatureScore:
      toNumber(
        data.temperature_score,
        0
      ),

    soilScore:
      toNumber(
        data.soil_score,
        0
      ),

    seasonScore:
      toNumber(
        data.season_score,
        0
      ),

    vegetationScore:
      toNumber(
        data.vegetation_score,
        0
      ),


    // -----------------------------------------------------
    // Explanation
    // -----------------------------------------------------

    whyRecommended:
      data.why_recommended ??
      data.explanation ??
      "",

    explanation:
      data.explanation ??
      data.why_recommended ??
      "",


    // -----------------------------------------------------
    // Crop comparison
    // -----------------------------------------------------

    comparison:
      (
        data.comparison ??
        []
      ).map((item) => ({
        crop:
          item.crop,

        score:
          toNumber(
            item.score,
            0
          ),

        reason:
          item.reason,
      })),


    // -----------------------------------------------------
    // Farm insights
    // -----------------------------------------------------

    farmInsights:
      data.farm_insights ??
      [],


    // -----------------------------------------------------
    // Weather risk
    // -----------------------------------------------------

    weatherRisk:
      data.weather_risk ??
      [],


    // -----------------------------------------------------
    // Satellite insights
    // -----------------------------------------------------

    satelliteInsights:
      data.satellite_insights ??
      [],


    // -----------------------------------------------------
    // Terrain insights
    // -----------------------------------------------------

    terrainInsights:
      data.terrain_insights ??
      [],


    // -----------------------------------------------------
    // Crop schedule
    // -----------------------------------------------------

    schedule:
      (
        data.schedule ??
        []
      ).map((stage) => ({
        stage:
          stage.stage,

        startDay:
          toNumber(
            stage.start_day,
            0
          ),

        endDay:
          toNumber(
            stage.end_day,
            0
          ),

        activities:
          stage.activities ??
          [],
      })),


    // -----------------------------------------------------
    // Farmer advice
    // -----------------------------------------------------

    farmerAdvice:
      data.farmer_advice ??
      [],


    // -----------------------------------------------------
    // Satellite availability
    // -----------------------------------------------------

    satelliteAvailable:
      Boolean(
        data.satellite_available ??
        data.satellite?.available ??
        false
      ),


    satellite,


    // -----------------------------------------------------
    // Topography
    // -----------------------------------------------------

    topography,


    // -----------------------------------------------------
    // Seven-day forecast
    // -----------------------------------------------------

    sevenDayForecast,
  };
}


// =========================================================
// API
// =========================================================

export async function getCropRecommendation(
  farmId: string,
  language: RecommendationLanguage = "en"
): Promise<CropRecommendation> {

  const response =
    await api.post<BackendCropRecommendation>(
      `/recommendations/crop/${farmId}`,

      null,

      {
        params: {
          language,
        },
      }
    );


  return normalizeCropRecommendation(
    response.data,
    language
  );
}