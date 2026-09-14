
// =========================================================
// LANGUAGE
// =========================================================

export type RecommendationLanguage =
  | "en"
  | "hi"
  | "bn";


// =========================================================
// CROP COMPARISON
// =========================================================

export interface CropComparison {
  crop: string;

  score: number;

  reason: string;
}


// =========================================================
// CROP SCHEDULE
// =========================================================

export interface CropScheduleStage {
  stage: string;

  startDay: number;

  endDay: number;

  activities: string[];
}


// =========================================================
// SATELLITE
// =========================================================

export interface SatelliteInsights {
  available: boolean;

  source?: string;

  acquisitionWindowDays?:
    number | null;

  ndvi?: number | null;

  ndmi?: number | null;

  bsi?: number | null;

  cloudMasked?: boolean;
}


// =========================================================
// TOPOGRAPHY
// =========================================================

export interface TopographyInsights {
  elevationM: number | null;

  source?: string;

  interpretation?: string;
}


// =========================================================
// WEATHER FORECAST
// =========================================================

export interface ForecastInsight {
  date: string;

  temperatureMax:
    number | null;

  temperatureMin:
    number | null;

  rainfall:
    number | null;

  precipitationProbability:
    number | null;

  weatherCode:
    number | null;
}


// =========================================================
// CROP RECOMMENDATION
// =========================================================

export interface CropRecommendation {

  // -------------------------------------------------------
  // Language
  // -------------------------------------------------------

  language:
    RecommendationLanguage;


  // -------------------------------------------------------
  // Crop recommendation
  // -------------------------------------------------------

  intendedCrop:
    string | null;

  recommendedCrop:
    string;

  recommendationScore:
    number;


  // -------------------------------------------------------
  // Existing component compatibility
  // -------------------------------------------------------

  crop:
    string;

  suitabilityScore:
    number;


  // -------------------------------------------------------
  // Score breakdown
  // -------------------------------------------------------

  rainfallScore:
    number;

  temperatureScore:
    number;

  soilScore:
    number;

  seasonScore:
    number;

  vegetationScore:
    number;


  // -------------------------------------------------------
  // AI explanation
  // -------------------------------------------------------

  whyRecommended:
    string;

  explanation:
    string;


  // -------------------------------------------------------
  // Comparison
  // -------------------------------------------------------

  comparison:
    CropComparison[];


  // -------------------------------------------------------
  // Farm intelligence
  // -------------------------------------------------------

  farmInsights:
    string[];

  weatherRisk:
    string[];

  satelliteInsights:
    string[];

  terrainInsights:
    string[];


  // -------------------------------------------------------
  // Crop lifecycle
  // -------------------------------------------------------

  schedule:
    CropScheduleStage[];


  farmerAdvice:
    string[];


  // -------------------------------------------------------
  // Satellite data
  // -------------------------------------------------------

  satelliteAvailable:
    boolean;

  satellite:
    SatelliteInsights | null;


  // -------------------------------------------------------
  // Terrain data
  // -------------------------------------------------------

  topography:
    TopographyInsights;


  // -------------------------------------------------------
  // Weather forecast
  // -------------------------------------------------------

  sevenDayForecast:
    ForecastInsight[];
}