"use client";

import {
  CloudRain,
  Droplets,
  Gauge,
  Wind,
} from "lucide-react";

import { WeatherData } from "@/types/weather";
import {
  getWeatherDescription,
  getWeatherIcon,
} from "@/lib/weather";
import { useLanguage } from "@/context/LanguageContext";

interface WeatherCardProps {
  weather: WeatherData;
}

function formatValue(
  value: number | null | undefined,
  suffix = ""
) {
  if (value === null || value === undefined) {
    return "—";
  }

  return `${Math.round(value)}${suffix}`;
}

export default function WeatherCard({
  weather,
}: WeatherCardProps) {
  const { language, t } = useLanguage();

  return (
    <section className="rounded-2xl border border-slate-200 bg-white">
      <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
        <div>
          <h2 className="font-semibold text-slate-900">
            {t("weather")}
          </h2>

          <p className="text-sm text-slate-500">
            {t("todayWeather")}
          </p>
        </div>

        <span className="text-3xl">
          {getWeatherIcon(weather.weatherCode)}
        </span>
      </div>

      <div className="p-5">
        <div className="flex items-end gap-3">
          <span className="text-5xl font-semibold tracking-tight text-slate-900">
            {formatValue(weather.temperature, "°")}
          </span>

          <div className="mb-1">
            <p className="font-medium text-slate-700">
              {getWeatherDescription(
                weather.weatherCode,
                language
              )}
            </p>

            <p className="text-xs text-slate-500">
              {t("todayWeather")}
            </p>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-2 gap-3">
          <WeatherMetric
            icon={<Droplets size={17} />}
            label={t("humidity")}
            value={formatValue(
              weather.humidity,
              "%"
            )}
          />

          <WeatherMetric
            icon={<CloudRain size={17} />}
            label={t("rainProbability")}
            value={formatValue(
              weather.precipitationProbability,
              "%"
            )}
          />

          <WeatherMetric
            icon={<Wind size={17} />}
            label={t("wind")}
            value={formatValue(
              weather.windSpeed,
              " km/h"
            )}
          />

          <WeatherMetric
            icon={<Gauge size={17} />}
            label={t("rainfall")}
            value={formatValue(
              weather.rainfall,
              " mm"
            )}
          />
        </div>
      </div>
    </section>
  );
}

function WeatherMetric({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl bg-slate-50 p-3">
      <div className="flex items-center gap-2 text-emerald-600">
        {icon}

        <span className="text-xs text-slate-500">
          {label}
        </span>
      </div>

      <p className="mt-2 text-sm font-semibold text-slate-900">
        {value}
      </p>
    </div>
  );
}