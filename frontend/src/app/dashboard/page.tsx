"use client";

import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  AlertCircle,
  MapPin,
} from "lucide-react";

import MapWrapper from "@/components/map/MapWrapper";
import WeatherCard from "@/components/dashboard/WeatherCard";
import WeatherForecast from "@/components/dashboard/WeatherForecast";
import CropRecommendation from "@/components/dashboard/CropRecommendation";

import {
  getFarms,
} from "@/lib/farmApi";

import {
  getFarmWeather,
} from "@/lib/weatherApi";

import {
  getCurrentUserDetails,
  BackendUser,
} from "@/lib/auth";

import {
  getCropRecommendation,
} from "@/lib/recommendationApi";

import {
  useFarmStore,
} from "@/store/farmStore";

import {
  useLanguage,
} from "@/context/LanguageContext";

import {
  WeatherResponse,
} from "@/types/weather";

import {
  CropRecommendation as CropRecommendationType,
  RecommendationLanguage,
} from "@/types/crop";

export default function DashboardPage() {
  const {
    t,
    language,
  } = useLanguage();

  const farms =
    useFarmStore(
      (state) =>
        state.farms
    );

  const selectedFarmId =
    useFarmStore(
      (state) =>
        state.selectedFarmId
    );

  const setFarms =
    useFarmStore(
      (state) =>
        state.setFarms
    );

  const [
    user,
    setUser,
  ] =
    useState<BackendUser | null>(
      null
    );

  const [
    userLoading,
    setUserLoading,
  ] =
    useState(true);

  const [
    userLocation,
    setUserLocation,
  ] =
    useState<
      [number, number] | undefined
    >(undefined);

  const [
    locationError,
    setLocationError,
  ] =
    useState("");

  const [
    farmsLoading,
    setFarmsLoading,
  ] =
    useState(true);

  const [
    farmsError,
    setFarmsError,
  ] =
    useState("");

  const [
    weather,
    setWeather,
  ] =
    useState<
      WeatherResponse | null
    >(null);

  const [
    weatherLoading,
    setWeatherLoading,
  ] =
    useState(false);

  const [
    weatherError,
    setWeatherError,
  ] =
    useState("");

  const [
    recommendation,
    setRecommendation,
  ] =
    useState<
      CropRecommendationType | null
    >(null);

  const [
    recommendationLoading,
    setRecommendationLoading,
  ] =
    useState(false);

  const [
    recommendationError,
    setRecommendationError,
  ] =
    useState("");

  /*
   * Load authenticated farmer.
   */
  useEffect(() => {
    let mounted = true;

    const loadUser =
      async () => {
        try {
          const currentUser =
            await getCurrentUserDetails();

          if (!mounted) {
            return;
          }

          setUser(
            currentUser
          );

          if (
            currentUser?.latitude !==
              null &&
            currentUser?.latitude !==
              undefined &&
            currentUser?.longitude !==
              null &&
            currentUser?.longitude !==
              undefined
          ) {
            setUserLocation([
              currentUser.latitude,
              currentUser.longitude,
            ]);
          }
        } catch (error) {
          console.error(
            "Failed to load farmer:",
            error
          );
        } finally {
          if (mounted) {
            setUserLoading(
              false
            );
          }
        }
      };

    loadUser();

    return () => {
      mounted = false;
    };
  }, []);

  /*
   * Load farms belonging to
   * the authenticated farmer.
   */
  useEffect(() => {
    let mounted = true;

    const loadFarms =
      async () => {
        try {
          setFarmsLoading(
            true
          );

          setFarmsError("");

          const farmData =
            await getFarms();

          if (!mounted) {
            return;
          }

          setFarms(
            farmData
          );
        } catch (error) {
          console.error(
            "Failed to load farms:",
            error
          );

          if (mounted) {
            setFarmsError(
              "Unable to load your farms. Please make sure the backend is running."
            );
          }
        } finally {
          if (mounted) {
            setFarmsLoading(
              false
            );
          }
        }
      };

    loadFarms();

    return () => {
      mounted = false;
    };
  }, [setFarms]);

  /*
   * Browser GPS.
   *
   * Saved farm/backend location
   * remains available if permission
   * is denied.
   */
  useEffect(() => {
    if (
      typeof navigator ===
        "undefined" ||
      !navigator.geolocation
    ) {
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const latitude =
          position.coords.latitude;

        const longitude =
          position.coords.longitude;

        setUserLocation([
          latitude,
          longitude,
        ]);

        setLocationError("");

        /*
         * Persist GPS location
         * through the authenticated API.
         */
        try {
          const {
            api,
          } = await import(
            "@/lib/api"
          );

          await api.patch(
            "/users/me/location",
            {
              latitude,
              longitude,
            }
          );
        } catch (error) {
          console.error(
            "Failed to save GPS location:",
            error
          );
        }
      },
      (error) => {
        console.warn(
          "Geolocation unavailable:",
          error
        );

        setLocationError(
          "Location permission was not granted. Using your saved farm location instead."
        );
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000,
      }
    );
  }, []);

  /*
   * Determine selected farm.
   */
  const selectedFarm =
    useMemo(() => {
      if (
        farms.length === 0
      ) {
        return undefined;
      }

      if (
        selectedFarmId
      ) {
        const matchingFarm =
          farms.find(
            (farm) =>
              farm.id ===
              selectedFarmId
          );

        if (
          matchingFarm
        ) {
          return matchingFarm;
        }
      }

      return farms[0];
    }, [
      farms,
      selectedFarmId,
    ]);

  /*
   * Load weather whenever
   * selected farm changes.
   */
  useEffect(() => {
    if (
      !selectedFarm
    ) {
      setWeather(null);
      return;
    }

    let mounted = true;

    const loadWeather =
      async () => {
        try {
          setWeatherLoading(
            true
          );

          setWeatherError("");

          const weatherData =
            await getFarmWeather(
              selectedFarm.id
            );

          if (mounted) {
            setWeather(
              weatherData
            );
          }
        } catch (error) {
          console.error(
            "Failed to load weather:",
            error
          );

          if (mounted) {
            setWeatherError(
              "Unable to load weather data for this farm."
            );

            setWeather(null);
          }
        } finally {
          if (mounted) {
            setWeatherLoading(
              false
            );
          }
        }
      };

    loadWeather();

    return () => {
      mounted = false;
    };
  }, [
    selectedFarm,
  ]);

  /*
   * Load AI recommendation.
   *
   * IMPORTANT:
   * The selected language is sent
   * to the backend.
   *
   * en -> English
   * hi -> Hindi
   * bn -> Bangla
   */
  useEffect(() => {
    if (
      !selectedFarm
    ) {
      setRecommendation(
        null
      );

      return;
    }

    let mounted = true;

    const loadRecommendation =
      async () => {
        try {
          setRecommendationLoading(
            true
          );

          setRecommendationError("");

          const recommendationData =
            await getCropRecommendation(
              selectedFarm.id,
              language as RecommendationLanguage
            );

          if (mounted) {
            setRecommendation(
              recommendationData
            );
          }
        } catch (error) {
          console.error(
            "Failed to load crop recommendation:",
            error
          );

          if (mounted) {
            setRecommendationError(
              "AI crop recommendation is currently unavailable."
            );

            setRecommendation(
              null
            );
          }
        } finally {
          if (mounted) {
            setRecommendationLoading(
              false
            );
          }
        }
      };

    loadRecommendation();

    return () => {
      mounted = false;
    };
  }, [
    selectedFarm,
    language,
  ]);

  /*
   * Map center priority:
   *
   * 1. Selected farm
   * 2. Browser GPS
   * 3. Map default
   */
  const mapCenter =
    selectedFarm
      ? ([
          selectedFarm.latitude,
          selectedFarm.longitude,
        ] as [
          number,
          number
        ])
      : userLocation;

  return (
    <div className="space-y-6">
      {/* Page heading */}
      <div>
        <p className="text-sm font-medium text-emerald-600">
          {t("overview")}
        </p>

        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900">
          {userLoading
            ? t("welcomeBack")
            : `${t(
                "welcomeBack"
              )}, ${
                user?.name ||
                t("farmer")
              }`}
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          {selectedFarm
            ? selectedFarm.name
            : t(
                "noFarmSelected"
              )}
        </p>
      </div>

      {/* Location notice */}
      {locationError && (
        <div className="flex items-start gap-3 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-700">
          <MapPin
            size={18}
            className="mt-0.5 shrink-0"
          />

          <p>
            {locationError}
          </p>
        </div>
      )}

      {/* Farms error */}
      {farmsError && (
        <div className="flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          <AlertCircle
            size={18}
            className="mt-0.5 shrink-0"
          />

          <p>
            {farmsError}
          </p>
        </div>
      )}

      {/* Farm overview */}
      <section className="rounded-2xl border border-slate-200 bg-white">
        <div className="border-b border-slate-200 px-5 py-4">
          <h2 className="font-semibold text-slate-900">
            {t("farmOverview")}
          </h2>

          <p className="text-sm text-slate-500">
            {selectedFarm
              ? selectedFarm.name
              : t(
                  "noFarmSelected"
                )}
          </p>
        </div>

        <div className="h-[520px] p-2">
          {farmsLoading ? (
            <div className="flex h-full min-h-[500px] items-center justify-center rounded-2xl bg-slate-100">
              <p className="text-sm text-slate-500">
                {t("loading")}
              </p>
            </div>
          ) : (
            <MapWrapper
              center={mapCenter}
              userLocation={
                userLocation
              }
              boundary={
                selectedFarm?.boundary
              }
            />
          )}
        </div>
      </section>

      {/* Weather + AI recommendation */}
      <div className="grid gap-6 xl:grid-cols-2">
        {/* Weather */}
        <div>
          {weatherLoading ? (
            <section className="flex min-h-[300px] items-center justify-center rounded-2xl border border-slate-200 bg-white">
              <p className="text-sm text-slate-500">
                {t("loading")}
              </p>
            </section>
          ) : weatherError ? (
            <section className="flex min-h-[300px] items-center gap-3 rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700">
              <AlertCircle
                size={18}
                className="shrink-0"
              />

              <p>
                {weatherError}
              </p>
            </section>
          ) : weather ? (
            <WeatherCard
              weather={
                weather.current
              }
            />
          ) : (
            <section className="flex min-h-[300px] items-center justify-center rounded-2xl border border-slate-200 bg-white">
              <p className="text-sm text-slate-500">
                {t(
                  "noFarmSelected"
                )}
              </p>
            </section>
          )}
        </div>

        {/* AI Recommendation */}
        <div>
          {recommendationLoading ? (
            <section className="flex min-h-[300px] flex-col items-center justify-center rounded-2xl border border-slate-200 bg-white">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-50 text-2xl">
                🌱
              </div>

              <p className="mt-3 text-sm font-medium text-slate-700">
                {t("loading")}
              </p>

              <p className="mt-1 text-xs text-slate-400">
                AI is analyzing weather, satellite and farm data...
              </p>
            </section>
          ) : recommendationError ? (
            <section className="flex min-h-[300px] items-center gap-3 rounded-2xl border border-amber-200 bg-amber-50 p-6 text-sm text-amber-700">
              <AlertCircle
                size={18}
                className="shrink-0"
              />

              <p>
                {
                  recommendationError
                }
              </p>
            </section>
          ) : recommendation ? (
            <CropRecommendation
              recommendation={
                recommendation
              }
            />
          ) : (
            <section className="flex min-h-[300px] items-center justify-center rounded-2xl border border-slate-200 bg-white">
              <p className="text-sm text-slate-500">
                {t(
                  "noFarmSelected"
                )}
              </p>
            </section>
          )}
        </div>
      </div>

      {/* Seven-day weather forecast */}
      {weather &&
        weather.daily &&
        weather.daily.length >
          0 && (
          <WeatherForecast
            daily={
              weather.daily
            }
          />
        )}
    </div>
  );
}