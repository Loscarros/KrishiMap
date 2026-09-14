
"use client";

import Link from "next/link";

import {
  ArrowUpRight,
  CheckCircle2,
  CloudRain,
  Mountain,
  Satellite,
  Sprout,
  Target,
  Thermometer,
  Wind,
} from "lucide-react";

import {
  CropRecommendation as CropRecommendationType,
} from "@/types/crop";

import { useLanguage } from "@/context/LanguageContext";


interface CropRecommendationProps {
  recommendation: CropRecommendationType;
}


// =========================================================
// COMPONENT
// =========================================================

export default function CropRecommendation({
  recommendation,
}: CropRecommendationProps) {

  const { t } = useLanguage();


  // =======================================================
  // Crop localization
  // =======================================================

  const getLocalizedCrop = (
    crop: string
  ) => {

    const cropMap: Record<
      string,
      | "rice"
      | "maize"
      | "wheat"
      | "potato"
      | "tomato"
      | "otherCrop"
    > = {
      Rice: "rice",
      Maize: "maize",
      Wheat: "wheat",
      Potato: "potato",
      Tomato: "tomato",
      Other: "otherCrop",
    };


    const key =
      cropMap[crop];


    return key
      ? t(key)
      : crop;
  };


  // =======================================================
  // Safe recommendation score
  // =======================================================

  const score = Math.min(
    100,
    Math.max(
      0,
      Number(
        recommendation.recommendationScore
      ) || 0
    )
  );


  // =======================================================
  // Satellite
  // =======================================================

  const satellite =
    recommendation.satellite;


  // =======================================================
  // Topography
  // =======================================================

  const elevation =
    recommendation.topography
      ?.elevationM;


  return (
    <section className="rounded-2xl border border-slate-200 bg-white">


      {/* ===================================================
          HEADER
      =================================================== */}

      <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">

        <div>

          <h2 className="font-semibold text-slate-900">
            {t("cropRecommendation")}
          </h2>

          <p className="text-sm text-slate-500">
            {t("automatedInterpretation")}
          </p>

        </div>


        <div className="rounded-xl bg-emerald-50 p-2 text-emerald-600">

          <Sprout size={20} />

        </div>

      </div>


      <div className="space-y-6 p-5">


        {/* =================================================
            MAIN RECOMMENDATION
        ================================================= */}

        <div className="rounded-2xl bg-emerald-50 p-5">

          <div className="flex items-center gap-4">

            <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-white text-3xl shadow-sm">
              🌾
            </div>


            <div className="min-w-0 flex-1">

              <p className="text-xs font-medium uppercase tracking-wider text-emerald-600">
                {t("cropRecommendation")}
              </p>


              <h3 className="mt-1 text-2xl font-semibold text-slate-900">

                {getLocalizedCrop(
                  recommendation.recommendedCrop
                )}

              </h3>


              {recommendation.explanation && (
                <p className="mt-1 text-sm leading-6 text-slate-600">
                  {recommendation.explanation}
                </p>
              )}

            </div>


            <div className="text-right">

              <p className="text-3xl font-semibold text-emerald-700">
                {score}
              </p>

              <p className="text-xs text-slate-500">
                {t("suitability")}
              </p>

            </div>

          </div>

        </div>


        {/* =================================================
            INTENDED CROP VS RECOMMENDED CROP
        ================================================= */}

        {recommendation.intendedCrop && (

          <div className="grid gap-3 sm:grid-cols-2">


            <div className="rounded-xl border border-slate-200 p-4">

              <div className="flex items-center gap-2">

                <Sprout
                  size={16}
                  className="text-slate-500"
                />

                <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                  Intended crop
                </p>

              </div>


              <p className="mt-2 text-lg font-semibold text-slate-900">

                {getLocalizedCrop(
                  recommendation.intendedCrop
                )}

              </p>

            </div>


            <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4">

              <div className="flex items-center gap-2">

                <Target
                  size={16}
                  className="text-emerald-600"
                />

                <p className="text-xs font-medium uppercase tracking-wide text-emerald-600">
                  Better suited crop
                </p>

              </div>


              <p className="mt-2 text-lg font-semibold text-emerald-800">

                {getLocalizedCrop(
                  recommendation.recommendedCrop
                )}

              </p>

            </div>

          </div>

        )}


        {/* =================================================
            WHY RECOMMENDED
        ================================================= */}

        {recommendation.whyRecommended && (

          <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">

            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
              AI farm insight
            </p>


            <p className="mt-2 text-sm leading-6 text-slate-700">
              {recommendation.whyRecommended}
            </p>

          </div>

        )}


        {/* =================================================
            CROP COMPARISON
        ================================================= */}

        {recommendation.comparison.length > 0 && (

          <div>

            <div className="mb-3">

              <h3 className="text-sm font-semibold text-slate-900">
                Crop suitability comparison
              </h3>

              <p className="text-xs text-slate-500">
                Comparison across the available crop candidates
              </p>

            </div>


            <div className="space-y-3">

              {recommendation.comparison.map(
                (item) => {

                  const itemScore =
                    Math.min(
                      100,
                      Math.max(
                        0,
                        Number(
                          item.score
                        ) || 0
                      )
                    );


                  const isWinner =
                    item.crop ===
                    recommendation.recommendedCrop;


                  return (

                    <div
                      key={item.crop}
                      className={`rounded-xl border p-3 ${
                        isWinner
                          ? "border-emerald-200 bg-emerald-50"
                          : "border-slate-200 bg-white"
                      }`}
                    >

                      <div className="flex items-center justify-between gap-3">

                        <div className="flex min-w-0 items-center gap-2">

                          {isWinner && (

                            <CheckCircle2
                              size={16}
                              className="shrink-0 text-emerald-600"
                            />

                          )}


                          <span className="text-sm font-medium text-slate-900">

                            {getLocalizedCrop(
                              item.crop
                            )}

                          </span>

                        </div>


                        <span className="text-sm font-semibold text-slate-900">

                          {itemScore}%

                        </span>

                      </div>


                      <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-100">

                        <div
                          className="h-full rounded-full bg-emerald-600 transition-all"
                          style={{
                            width:
                              `${itemScore}%`,
                          }}
                        />

                      </div>


                      {item.reason && (

                        <p className="mt-2 text-xs leading-5 text-slate-500">
                          {item.reason}
                        </p>

                      )}

                    </div>

                  );

                }
              )}

            </div>

          </div>

        )}


        {/* =================================================
            SCORE BREAKDOWN
        ================================================= */}

        <div>

          <h3 className="mb-3 text-sm font-semibold text-slate-900">
            Suitability breakdown
          </h3>


          <div className="space-y-4">

            <ScoreBar
              label={t(
                "rainfallSuitability"
              )}
              value={
                recommendation.rainfallScore
              }
            />


            <ScoreBar
              label={t(
                "temperatureSuitability"
              )}
              value={
                recommendation.temperatureScore
              }
            />


            <ScoreBar
              label={t(
                "soilSuitability"
              )}
              value={
                recommendation.soilScore
              }
            />


            <ScoreBar
              label={t(
                "seasonSuitability"
              )}
              value={
                recommendation.seasonScore
              }
            />


            <ScoreBar
              label={t(
                "vegetationSuitability"
              )}
              value={
                recommendation.vegetationScore
              }
            />

          </div>

        </div>


        {/* =================================================
            WEATHER RISK
        ================================================= */}

        {recommendation.weatherRisk.length > 0 && (

          <div>

            <div className="mb-3 flex items-center gap-2">

              <CloudRain
                size={17}
                className="text-emerald-600"
              />

              <div>

                <h3 className="text-sm font-semibold text-slate-900">
                  Weather risk
                </h3>

                <p className="text-xs text-slate-500">
                  Based on the current weather and seven-day forecast
                </p>

              </div>

            </div>


            <div className="space-y-2">

              {recommendation.weatherRisk.map(
                (risk, index) => (

                  <div
                    key={`${index}-${risk}`}
                    className="rounded-xl border border-amber-100 bg-amber-50 p-3"
                  >

                    <p className="text-sm leading-5 text-slate-700">
                      {risk}
                    </p>

                  </div>

                )
              )}

            </div>

          </div>

        )}


        {/* =================================================
            SATELLITE + TOPOGRAPHY
        ================================================= */}

        <div className="grid gap-3 sm:grid-cols-2">


          {/* Satellite */}

          <div className="rounded-xl border border-slate-200 p-4">

            <div className="flex items-center gap-2">

              <Satellite
                size={17}
                className="text-emerald-600"
              />

              <p className="text-sm font-semibold text-slate-900">
                Satellite insights
              </p>

            </div>


            {recommendation.satelliteAvailable &&
            satellite ? (

              <>

                <div className="mt-4 grid grid-cols-3 gap-2">

                  <Indicator
                    label="NDVI"
                    value={
                      satellite.ndvi
                    }
                  />

                  <Indicator
                    label="NDMI"
                    value={
                      satellite.ndmi
                    }
                  />

                  <Indicator
                    label="BSI"
                    value={
                      satellite.bsi
                    }
                  />

                </div>


                {satellite.source && (

                  <p className="mt-3 text-[11px] leading-4 text-slate-400">
                    Source: {satellite.source}
                  </p>

                )}


                {satellite.acquisitionWindowDays && (

                  <p className="mt-1 text-[11px] text-slate-400">
                    Observation window: last{" "}
                    {
                      satellite.acquisitionWindowDays
                    }{" "}
                    days
                  </p>

                )}

              </>

            ) : (

              <div className="mt-3 rounded-lg bg-slate-50 p-3">

                <p className="text-xs leading-5 text-slate-500">
                  Satellite observations are currently unavailable for this farm.
                </p>

              </div>

            )}

          </div>


          {/* Topography */}

          <div className="rounded-xl border border-slate-200 p-4">

            <div className="flex items-center gap-2">

              <Mountain
                size={17}
                className="text-emerald-600"
              />

              <p className="text-sm font-semibold text-slate-900">
                Topography
              </p>

            </div>


            <p className="mt-4 text-2xl font-semibold text-slate-900">

              {elevation !== null &&
              elevation !== undefined
                ? `${elevation.toFixed(0)} m`
                : "—"}

            </p>


            <p className="mt-1 text-xs text-slate-500">
              Farm elevation
            </p>


            {recommendation.topography
              ?.source && (

              <p className="mt-2 text-[11px] leading-4 text-slate-400">
                Source:{" "}
                {
                  recommendation.topography
                    .source
                }
              </p>

            )}

          </div>

        </div>


        {/* =================================================
            SATELLITE INTERPRETATION
        ================================================= */}

        {recommendation.satelliteInsights.length >
          0 && (

          <div>

            <div className="mb-3 flex items-center gap-2">

              <Satellite
                size={17}
                className="text-emerald-600"
              />

              <h3 className="text-sm font-semibold text-slate-900">
                Satellite interpretation
              </h3>

            </div>


            <div className="space-y-2">

              {recommendation.satelliteInsights.map(
                (insight, index) => (

                  <div
                    key={`${index}-${insight}`}
                    className="rounded-xl bg-slate-50 p-3"
                  >

                    <p className="text-sm leading-5 text-slate-600">
                      {insight}
                    </p>

                  </div>

                )
              )}

            </div>

          </div>

        )}


        {/* =================================================
            TERRAIN INSIGHTS
        ================================================= */}

        {recommendation.terrainInsights.length >
          0 && (

          <div>

            <div className="mb-3 flex items-center gap-2">

              <Mountain
                size={17}
                className="text-emerald-600"
              />

              <h3 className="text-sm font-semibold text-slate-900">
                Terrain insights
              </h3>

            </div>


            <div className="space-y-2">

              {recommendation.terrainInsights.map(
                (insight, index) => (

                  <div
                    key={`${index}-${insight}`}
                    className="rounded-xl bg-slate-50 p-3"
                  >

                    <p className="text-sm leading-5 text-slate-600">
                      {insight}
                    </p>

                  </div>

                )
              )}

            </div>

          </div>

        )}


        {/* =================================================
            SEVEN DAY FORECAST
        ================================================= */}

        {recommendation.sevenDayForecast.length >
          0 && (

          <div>

            <div className="mb-3 flex items-center justify-between">

              <div>

                <h3 className="text-sm font-semibold text-slate-900">
                  Seven-day forecast
                </h3>

                <p className="text-xs text-slate-500">
                  Weather conditions used by the recommendation engine
                </p>

              </div>

            </div>


            <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">

              {recommendation.sevenDayForecast.map(
                (day) => (

                  <ForecastCard
                    key={day.date}
                    date={day.date}
                    temperatureMax={
                      day.temperatureMax
                    }
                    temperatureMin={
                      day.temperatureMin
                    }
                    rainfall={
                      day.rainfall
                    }
                    precipitationProbability={
                      day.precipitationProbability
                    }
                  />

                )
              )}

            </div>

          </div>

        )}


        {/* =================================================
            FARM INSIGHTS
        ================================================= */}

        {recommendation.farmInsights.length >
          0 && (

          <div>

            <h3 className="mb-3 text-sm font-semibold text-slate-900">
              Farm insights
            </h3>


            <div className="space-y-2">

              {recommendation.farmInsights.map(
                (insight, index) => (

                  <div
                    key={`${index}-${insight}`}
                    className="flex gap-2 rounded-xl bg-slate-50 p-3"
                  >

                    <CheckCircle2
                      size={16}
                      className="mt-0.5 shrink-0 text-emerald-600"
                    />

                    <p className="text-sm leading-5 text-slate-600">
                      {insight}
                    </p>

                  </div>

                )
              )}

            </div>

          </div>

        )}


        {/* =================================================
            FARMER ADVICE
        ================================================= */}

        {recommendation.farmerAdvice.length >
          0 && (

          <div>

            <h3 className="mb-3 text-sm font-semibold text-slate-900">
              Farmer advice
            </h3>


            <div className="space-y-2">

              {recommendation.farmerAdvice.map(
                (advice, index) => (

                  <div
                    key={`${index}-${advice}`}
                    className="rounded-xl border border-emerald-100 bg-emerald-50 p-3"
                  >

                    <p className="text-sm leading-5 text-slate-700">
                      {advice}
                    </p>

                  </div>

                )
              )}

            </div>

          </div>

        )}


        {/* =================================================
            CROP LIFECYCLE
        ================================================= */}

        {recommendation.schedule.length >
          0 && (

          <div>

            <div className="mb-3">

              <h3 className="text-sm font-semibold text-slate-900">
                Crop lifecycle
              </h3>

              <p className="text-xs text-slate-500">
                Approximate relative stages from planting day
              </p>

            </div>


            <div className="space-y-3">

              {recommendation.schedule.map(
                (stage, index) => (

                  <div
                    key={`${stage.stage}-${index}`}
                    className="rounded-xl border border-slate-200 p-4"
                  >

                    <div className="flex items-center justify-between gap-3">

                      <p className="text-sm font-semibold capitalize text-slate-900">
                        {stage.stage}
                      </p>


                      <span className="shrink-0 rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-medium text-emerald-700">

                        Day{" "}
                        {stage.startDay}
                        –
                        {stage.endDay}

                      </span>

                    </div>


                    {stage.activities.length >
                      0 && (

                      <ul className="mt-3 space-y-1.5">

                        {stage.activities.map(
                          (
                            activity,
                            activityIndex
                          ) => (

                            <li
                              key={`${activityIndex}-${activity}`}
                              className="text-xs leading-5 text-slate-600"
                            >
                              • {activity}
                            </li>

                          )
                        )}

                      </ul>

                    )}

                  </div>

                )
              )}

            </div>

          </div>

        )}


        {/* =================================================
            CONFIRMATION
        ================================================= */}

        <div className="flex items-center gap-2 rounded-xl border border-emerald-100 bg-white p-3 text-xs text-slate-500">

          <CheckCircle2
            size={16}
            className="shrink-0 text-emerald-600"
          />

          <span>
            {t(
              "automatedInterpretation"
            )}
          </span>

        </div>


        {/* =================================================
            ANALYSIS LINK
        ================================================= */}

        <Link
          href="/dashboard/analysis"
          className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 px-4 py-3 text-sm font-medium text-slate-700 transition hover:border-emerald-300 hover:bg-emerald-50 hover:text-emerald-700"
        >

          {t("farmAnalysis")}

          <ArrowUpRight
            size={16}
          />

        </Link>

      </div>

    </section>
  );
}


// =========================================================
// SCORE BAR
// =========================================================

function ScoreBar({
  label,
  value,
}: {
  label: string;
  value: number;
}) {

  const safeValue =
    Math.min(
      100,
      Math.max(
        0,
        Number(value) || 0
      )
    );


  return (

    <div>

      <div className="mb-1.5 flex items-center justify-between">

        <span className="text-sm text-slate-600">
          {label}
        </span>

        <span className="text-sm font-medium text-slate-900">
          {safeValue}%
        </span>

      </div>


      <div className="h-2 overflow-hidden rounded-full bg-slate-100">

        <div
          className="h-full rounded-full bg-emerald-600 transition-all"
          style={{
            width:
              `${safeValue}%`,
          }}
        />

      </div>

    </div>
  );
}


// =========================================================
// SATELLITE INDICATOR
// =========================================================

function Indicator({
  label,
  value,
}: {
  label: string;
  value?: number | null;
}) {

  return (

    <div className="rounded-lg bg-slate-50 p-2 text-center">

      <p className="text-[10px] font-medium uppercase tracking-wide text-slate-400">
        {label}
      </p>


      <p className="mt-1 text-sm font-semibold text-slate-900">

        {value !== null &&
        value !== undefined
          ? value.toFixed(2)
          : "—"}

      </p>

    </div>
  );
}


// =========================================================
// FORECAST CARD
// =========================================================

function ForecastCard({
  date,
  temperatureMax,
  temperatureMin,
  rainfall,
  precipitationProbability,
}: {
  date: string;

  temperatureMax:
    number | null;

  temperatureMin:
    number | null;

  rainfall:
    number | null;

  precipitationProbability:
    number | null;
}) {

  const formattedDate =
    new Date(
      `${date}T12:00:00`
    ).toLocaleDateString(
      undefined,
      {
        weekday: "short",
        day: "numeric",
        month: "short",
      }
    );


  return (

    <div className="rounded-xl border border-slate-200 bg-white p-3">

      <p className="text-xs font-medium text-slate-500">
        {formattedDate}
      </p>


      <div className="mt-3 flex items-center gap-2">

        <Thermometer
          size={15}
          className="text-emerald-600"
        />

        <p className="text-sm font-semibold text-slate-900">

          {temperatureMax !== null
            ? `${temperatureMax.toFixed(0)}°`
            : "—"}

          <span className="ml-1 font-normal text-slate-400">

            {temperatureMin !== null
              ? `/ ${temperatureMin.toFixed(0)}°`
              : ""}

          </span>

        </p>

      </div>


      <div className="mt-2 flex items-center gap-2">

        <CloudRain
          size={14}
          className="text-slate-400"
        />

        <p className="text-xs text-slate-600">

          {rainfall !== null
            ? `${rainfall.toFixed(1)} mm`
            : "—"}

        </p>

      </div>


      <div className="mt-1 flex items-center gap-2">

        <Wind
          size={14}
          className="text-slate-400"
        />

        <p className="text-xs text-slate-600">

          {precipitationProbability !== null
            ? `${precipitationProbability.toFixed(0)}% rain`
            : "—"}

        </p>

      </div>

    </div>
  );
}