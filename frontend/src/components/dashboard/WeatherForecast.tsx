"use client";

import { DailyWeather } from "@/types/weather";
import {
  getWeatherDescription,
  getWeatherIcon,
} from "@/lib/weather";
import { useLanguage } from "@/context/LanguageContext";

interface WeatherForecastProps {
  daily: DailyWeather[];
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

export default function WeatherForecast({
  daily,
}: WeatherForecastProps) {
  const { language, t } = useLanguage();

  const locale =
    language === "hi"
      ? "hi-IN"
      : language === "bn"
      ? "bn-IN"
      : "en-IN";

  return (
    <section className="rounded-2xl border border-slate-200 bg-white">
      <div className="border-b border-slate-200 px-5 py-4">
        <h2 className="font-semibold text-slate-900">
          {t("weatherForecast")}
        </h2>

        <p className="text-sm text-slate-500">
          {t("sevenDayForecast")}
        </p>
      </div>

      <div className="grid grid-cols-2 divide-x divide-y divide-slate-100 md:grid-cols-4 xl:grid-cols-7 xl:divide-y-0">
        {daily.map((day) => {
          const date = new Date(
            `${day.date}T00:00:00`
          );

          return (
            <div
              key={day.date}
              className="p-4 text-center"
            >
              <p className="text-xs font-medium text-slate-500">
                {date.toLocaleDateString(
                  locale,
                  {
                    weekday: "short",
                  }
                )}
              </p>

              <p className="mt-1 text-xs text-slate-400">
                {date.toLocaleDateString(
                  locale,
                  {
                    day: "numeric",
                    month: "short",
                  }
                )}
              </p>

              <div className="my-4 text-3xl">
                {getWeatherIcon(
                  day.weatherCode
                )}
              </div>

              <p className="text-xs text-slate-500">
                {getWeatherDescription(
                  day.weatherCode,
                  language
                )}
              </p>

              <div className="mt-3">
                <span className="font-semibold text-slate-900">
                  {formatValue(
                    day.temperatureMax,
                    "°"
                  )}
                </span>

                <span className="ml-2 text-sm text-slate-400">
                  {formatValue(
                    day.temperatureMin,
                    "°"
                  )}
                </span>
              </div>

              <div className="mt-3 rounded-lg bg-blue-50 px-2 py-1">
                <p className="text-xs font-medium text-blue-700">
                  💧{" "}
                  {formatValue(
                    day.precipitationProbability,
                    "%"
                  )}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}