"use client";

import { useEffect, useMemo, useState } from "react";

import {
  Activity,
  Droplets,
  Leaf,
  MapPin,
  Sprout,
  Thermometer,
  TrendingUp,
  Wind,
} from "lucide-react";

import MapWrapper from "@/components/map/MapWrapper";
import { getFarmWeather } from "@/lib/weatherApi";
import { useFarmStore } from "@/store/farmStore";
import { useLanguage } from "@/context/LanguageContext";
import { WeatherResponse } from "@/types/weather";

function ScoreBar({
  label,
  value,
  icon: Icon,
}: {
  label: string;
  value: number;
  icon: React.ElementType;
}) {
  const safeValue = Math.min(100, Math.max(0, value));

  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon size={16} className="text-emerald-600" />

          <span className="text-sm font-medium text-slate-700">
            {label}
          </span>
        </div>

        <span className="text-sm font-semibold text-slate-900">
          {safeValue}%
        </span>
      </div>

      <div className="h-2 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-emerald-500 transition-all"
          style={{
            width: `${safeValue}%`,
          }}
        />
      </div>
    </div>
  );
}

function MetricCard({
  title,
  value,
  suffix,
  description,
  icon: Icon,
}: {
  title: string;
  value: string;
  suffix?: string;
  description: string;
  icon: React.ElementType;
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-500">{title}</p>

          <div className="mt-2 flex items-end gap-1">
            <span className="text-3xl font-semibold text-slate-900">
              {value}
            </span>

            {suffix && (
              <span className="mb-1 text-sm text-slate-500">
                {suffix}
              </span>
            )}
          </div>
        </div>

        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
          <Icon size={20} />
        </div>
      </div>

      <p className="mt-3 text-xs text-slate-500">{description}</p>
    </div>
  );
}

export default function AnalysisPage() {
  const { t } = useLanguage();

  const farms = useFarmStore((state) => state.farms);

  const selectedFarmId = useFarmStore(
    (state) => state.selectedFarmId
  );

  const selectedFarm = farms.find(
    (farm) => farm.id === selectedFarmId
  );

  const [weather, setWeather] =
    useState<WeatherResponse | null>(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState(false);

  useEffect(() => {
    /*
     * Important:
     * selectedFarmId can be null, so we explicitly
     * stop before calling the API.
     */
    if (!selectedFarmId) {
      setWeather(null);
      setLoading(false);
      setError(false);
      return;
    }

    /*
     * After the guard above, TypeScript knows that
     * selectedFarmId is a string inside this effect.
     */
    const farmId = selectedFarmId;

    let mounted = true;

    async function loadWeather() {
      try {
        setLoading(true);
        setError(false);

        const data = await getFarmWeather(farmId);

        if (mounted) {
          setWeather(data);
        }
      } catch (err) {
        console.error(
          "Failed to load analysis weather:",
          err
        );

        if (mounted) {
          setWeather(null);
          setError(true);
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    loadWeather();

    return () => {
      mounted = false;
    };
  }, [selectedFarmId]);

  const analysis = useMemo(() => {
    if (!weather) {
      return {
        cropHealth: 0,
        vegetation: 0,
        soilSuitability: 0,
        weatherSuitability: 0,
        irrigationNeed: 0,
        overallScore: 0,
      };
    }

    const current = weather.current;

    /*
     * These are transparent weather-based
     * indicators for the current prototype.
     *
     * Soil and satellite/NDVI data are NOT
     * available yet, so we don't pretend they
     * are real measurements.
     */

    const temperature = current.temperature ?? 25;

    const humidity = current.humidity ?? 60;

    const rainProbability =
      current.precipitationProbability ?? 0;

    const rainfall = current.rainfall ?? 0;

    // Temperature suitability.
    const temperatureScore = Math.min(
      100,
      Math.max(
        0,
        100 - Math.abs(temperature - 25) * 4
      )
    );

    // Humidity suitability.
    const humidityScore = Math.min(
      100,
      Math.max(
        0,
        100 - Math.abs(humidity - 65) * 1.5
      )
    );

    // Rainfall suitability.
    const rainfallScore =
      rainProbability > 70
        ? 85
        : rainProbability > 40
        ? 78
        : rainfall > 0
        ? 70
        : 55;

    const weatherSuitability = Math.round(
      temperatureScore * 0.6 +
        humidityScore * 0.2 +
        rainfallScore * 0.2
    );

    /*
     * Until satellite/NDVI and soil APIs
     * are connected, vegetation and soil
     * values remain neutral rather than
     * fabricated.
     */
    const vegetation = 50;
    const soilSuitability = 50;

    const cropHealth = Math.round(
      weatherSuitability * 0.65 +
        vegetation * 0.35
    );

    /*
     * Higher rain probability/rainfall means
     * lower immediate irrigation requirement.
     */
    const irrigationNeed = Math.round(
      Math.min(
        100,
        Math.max(
          0,
          100 -
            rainProbability * 0.7 -
            rainfall * 8
        )
      )
    );

    const overallScore = Math.round(
      cropHealth * 0.35 +
        vegetation * 0.15 +
        soilSuitability * 0.15 +
        weatherSuitability * 0.35
    );

    return {
      cropHealth,
      vegetation,
      soilSuitability,
      weatherSuitability,
      irrigationNeed,
      overallScore,
    };
  }, [weather]);

  const getLocalizedCrop = (crop?: string) => {
    if (!crop) {
      return t("rice");
    }

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

    const key = cropMap[crop];

    return key ? t(key) : crop;
  };

  if (!selectedFarm) {
    return (
      <div className="flex min-h-[70vh] items-center justify-center">
        <div className="text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-600">
            <MapPin size={24} />
          </div>

          <h1 className="mt-4 text-xl font-semibold text-slate-900">
            {t("noFarmSelected")}
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            {t("addFirstFarm")}
          </p>
        </div>
      </div>
    );
  }

  const overallCondition =
    analysis.overallScore >= 80
      ? t("good")
      : analysis.overallScore >= 60
      ? t("moderate")
      : t("low");

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700">
            <Sprout size={22} />
          </div>

          <div>
            <h1 className="text-2xl font-semibold text-slate-900">
              {t("farmAnalysis")}
            </h1>

            <p className="mt-1 text-sm text-slate-500">
              {t("automatedInterpretation")}{" "}
              <span className="font-medium text-slate-700">
                {selectedFarm.name}
              </span>
            </p>
          </div>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-500">
          {t("loading")}...
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          Unable to load live weather analysis.
        </div>
      )}

      {/* Overall Score */}
      <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
        <div className="grid lg:grid-cols-[280px_1fr]">
          <div className="flex flex-col items-center justify-center border-b border-slate-200 bg-emerald-50/60 p-8 text-center lg:border-b-0 lg:border-r">
            <div className="relative flex h-40 w-40 items-center justify-center rounded-full border-[14px] border-emerald-100">
              <div
                className="absolute inset-0 rounded-full border-[14px] border-transparent border-t-emerald-500 border-r-emerald-500"
                style={{
                  transform: `rotate(${
                    analysis.overallScore * 1.8 - 90
                  }deg)`,
                }}
              />

              <div>
                <p className="text-4xl font-bold text-slate-900">
                  {analysis.overallScore}
                </p>

                <p className="text-xs font-medium uppercase tracking-wider text-slate-500">
                  {t("overall")}
                </p>
              </div>
            </div>

            <div className="mt-5">
              <p className="font-semibold text-emerald-700">
                {overallCondition}
              </p>

              <p className="mt-1 text-xs text-slate-500">
                {weather
                  ? t("overallDescription")
                  : t("loading")}
              </p>
            </div>
          </div>

          <div className="p-7">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-slate-900">
                  {t("farmHealthOverview")}
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  {t("overallDescription")}
                </p>
              </div>

              <div className="hidden items-center gap-2 rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-medium text-emerald-700 sm:flex">
                <TrendingUp size={14} />
                {t("positive")}
              </div>
            </div>

            <div className="mt-7 space-y-5">
              <ScoreBar
                label={t("cropHealth")}
                value={analysis.cropHealth}
                icon={Leaf}
              />

              <ScoreBar
                label={t("vegetationIndex")}
                value={analysis.vegetation}
                icon={Activity}
              />

              <ScoreBar
                label={t("soilSuitability")}
                value={analysis.soilSuitability}
                icon={Sprout}
              />

              <ScoreBar
                label={t("weatherSuitability")}
                value={analysis.weatherSuitability}
                icon={Thermometer}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Metrics */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          title={t("cropHealth")}
          value={`${analysis.cropHealth}`}
          suffix="%"
          description={t("healthy")}
          icon={Leaf}
        />

        <MetricCard
          title={t("vegetationIndex")}
          value={`${analysis.vegetation}`}
          suffix="%"
          description={
            weather
              ? t("vegetationIndex")
              : t("loading")
          }
          icon={Activity}
        />

        <MetricCard
          title={t("weatherSuitability")}
          value={`${analysis.weatherSuitability}`}
          suffix="%"
          description={t("weatherSuitability")}
          icon={Thermometer}
        />

        <MetricCard
          title={t("irrigationNeed")}
          value={`${analysis.irrigationNeed}`}
          suffix="%"
          description={t("moderate")}
          icon={Droplets}
        />
      </div>

      {/* Map + Insights */}
      <div className="grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
        <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
          <div className="border-b border-slate-200 px-5 py-4">
            <div className="flex items-center gap-2">
              <MapPin
                size={18}
                className="text-emerald-600"
              />

              <div>
                <h2 className="font-semibold text-slate-900">
                  {t("farmLocation")}
                </h2>

                <p className="text-xs text-slate-500">
                  {t("spatialOverview")}
                </p>
              </div>
            </div>
          </div>

          <div className="h-[420px] p-2">
            <MapWrapper
              center={[
                selectedFarm.latitude,
                selectedFarm.longitude,
              ]}
              boundary={selectedFarm.boundary}
            />
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-6">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700">
              🤖
            </div>

            <div>
              <h2 className="font-semibold text-slate-900">
                {t("aiFarmInsight")}
              </h2>

              <p className="text-xs text-slate-500">
                {t("automatedInterpretation")}
              </p>
            </div>
          </div>

          <div className="mt-6 rounded-2xl bg-slate-50 p-5">
            <p className="text-sm leading-6 text-slate-600">
              {weather
                ? t("overallDescription")
                : t("loading")}
            </p>

            <p className="mt-4 text-sm leading-6 text-slate-600">
              {t("weatherSuitability")}:{" "}
              {analysis.weatherSuitability}%
            </p>
          </div>

          <div className="mt-5 space-y-3">
            <div className="flex items-center justify-between rounded-xl border border-slate-200 p-3">
              <div className="flex items-center gap-3">
                <Droplets
                  size={17}
                  className="text-blue-500"
                />

                <span className="text-sm text-slate-600">
                  {t("irrigationNeed")}
                </span>
              </div>

              <span className="rounded-full bg-amber-50 px-2.5 py-1 text-xs font-medium text-amber-700">
                {analysis.irrigationNeed}%
              </span>
            </div>

            <div className="flex items-center justify-between rounded-xl border border-slate-200 p-3">
              <div className="flex items-center gap-3">
                <Wind
                  size={17}
                  className="text-slate-500"
                />

                <span className="text-sm text-slate-600">
                  Wind Risk
                </span>
              </div>

              <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-medium text-emerald-700">
                {weather &&
                (weather.current.windSpeed ?? 0) >
                  30
                  ? "High"
                  : t("low")}
              </span>
            </div>

            <div className="flex items-center justify-between rounded-xl border border-slate-200 p-3">
              <div className="flex items-center gap-3">
                <Leaf
                  size={17}
                  className="text-emerald-600"
                />

                <span className="text-sm text-slate-600">
                  {t("cropHealth")}
                </span>
              </div>

              <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-medium text-emerald-700">
                {analysis.cropHealth}%
              </span>
            </div>
          </div>
        </section>
      </div>

      {/* Recommendation */}
      <section className="rounded-2xl border border-emerald-200 bg-emerald-50/60 p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="flex items-center gap-2">
              <Sprout
                size={19}
                className="text-emerald-600"
              />

              <h2 className="font-semibold text-slate-900">
                {t("currentCropRecommendation")}
              </h2>
            </div>

            <p className="mt-2 text-sm text-slate-600">
              {t("currentCropRecommendation")}:{" "}
              <span className="font-semibold text-slate-900">
                {getLocalizedCrop(selectedFarm.crop)}
              </span>
            </p>
          </div>

          <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-white text-xl font-bold text-emerald-700 shadow-sm">
            {analysis.overallScore}
          </div>
        </div>
      </section>
    </div>
  );
}