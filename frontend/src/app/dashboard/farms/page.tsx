
"use client";

import { useState } from "react";

import {
  ArrowLeft,
  Check,
  MapPin,
  Sprout,
} from "lucide-react";

import Link from "next/link";

import MapWrapper from "@/components/map/MapWrapper";

import { createFarm } from "@/lib/farmApi";

import { useFarmStore } from "@/store/farmStore";

import { useLanguage } from "@/context/LanguageContext";

export default function FarmsPage() {
  const { t } = useLanguage();

  const addFarm =
    useFarmStore(
      (state) => state.addFarm
    );

  const [
    farmName,
    setFarmName,
  ] = useState("");

  const [
    crop,
    setCrop,
  ] = useState("");

  const [
    areaAcres,
    setAreaAcres,
  ] = useState(0);

  const [
    center,
    setCenter,
  ] = useState<
    [number, number] | null
  >(null);

  const [
    boundary,
    setBoundary,
  ] = useState<
    GeoJSON.Polygon | null
  >(null);

  const [
    saved,
    setSaved,
  ] = useState(false);

  const [
    saving,
    setSaving,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");

  const handleFarmDrawn = (
    polygon: GeoJSON.Polygon,
    area: number,
    mapCenter: [number, number]
  ) => {
    setBoundary(polygon);

    setAreaAcres(area);

    setCenter(mapCenter);

    setSaved(false);

    setError("");
  };

  const handleSave = async () => {
    /*
     * Validate everything before sending
     * the request to FastAPI.
     */
    if (
      !farmName.trim() ||
      !boundary ||
      !center ||
      areaAcres <= 0
    ) {
      setError(
        "Please enter a farm name and draw a valid farm boundary."
      );

      return;
    }

    try {
      setSaving(true);

      setSaved(false);

      setError("");

      /*
       * createFarm() sends:
       *
       * POST /api/farms
       *
       * The JWT is automatically attached
       * by the Axios interceptor.
       */
      const newFarm =
        await createFarm({
          name: farmName.trim(),

          areaAcres,

          latitude: center[0],

          longitude: center[1],

          boundary,

          crop:
            crop || undefined,
        });

      /*
       * IMPORTANT:
       *
       * newFarm.id comes from PostgreSQL.
       *
       * We do not create a frontend ID.
       */
      addFarm(newFarm);

      setSaved(true);

      /*
       * Clear the form after the database
       * has successfully confirmed creation.
       */
      setFarmName("");

      setCrop("");

      setBoundary(null);

      setAreaAcres(0);

      setCenter(null);
    } catch (error) {
      console.error(
        "Failed to save farm:",
        error
      );

      setError(
        "Unable to save the farm. Please make sure you are logged in and the backend is running."
      );
    } finally {
      setSaving(false);
    }
  };

  const cropOptions = [
    {
      value: "Rice",
      label: t("rice"),
    },
    {
      value: "Maize",
      label: t("maize"),
    },
    {
      value: "Wheat",
      label: t("wheat"),
    },
    {
      value: "Potato",
      label: t("potato"),
    },
    {
      value: "Tomato",
      label: t("tomato"),
    },
    {
      value: "Other",
      label: t("otherCrop"),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link
          href="/dashboard"
          className="rounded-xl border border-slate-200 bg-white p-2 text-slate-600 transition hover:bg-slate-50"
          title={t("dashboard")}
          aria-label={t("dashboard")}
        >
          <ArrowLeft size={18} />
        </Link>

        <div>
          <h1 className="text-2xl font-semibold text-slate-900">
            {t("addNewFarm")}
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            {t("drawFarmBoundary")}
          </p>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_360px]">
        {/* Map */}
        <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
          <div className="border-b border-slate-200 px-5 py-4">
            <div className="flex items-center gap-2">
              <MapPin
                size={18}
                className="text-emerald-600"
              />

              <div>
                <h2 className="font-semibold text-slate-900">
                  {t("farmBoundary")}
                </h2>

                <p className="text-xs text-slate-500">
                  {t("drawFarmBoundary")}
                </p>
              </div>
            </div>
          </div>

          <div className="h-[600px] p-2">
            <MapWrapper
              onFarmDrawn={
                handleFarmDrawn
              }
            />
          </div>
        </section>

        {/* Farm Details */}
        <section className="h-fit rounded-2xl border border-slate-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-slate-900">
            {t("farmDetails")}
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            {t("basicInformation")}
          </p>

          <div className="mt-6 space-y-5">
            {/* Farm Name */}
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">
                {t("farmName")}
              </label>

              <input
                value={farmName}
                onChange={(event) =>
                  setFarmName(
                    event.target.value
                  )
                }
                placeholder={
                  t("farmName") ===
                  "Farm name"
                    ? "e.g. North Field"
                    : t("farmName")
                }
                className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
              />
            </div>

            {/* Crop */}
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">
                {t("currentCrop")}
              </label>

              <div className="relative">
                <Sprout
                  size={17}
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                />

                <select
                  value={crop}
                  onChange={(event) =>
                    setCrop(
                      event.target.value
                    )
                  }
                  className="w-full appearance-none rounded-xl border border-slate-200 bg-white px-10 py-3 text-sm text-slate-700 outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
                >
                  <option value="">
                    {t("selectCrop")}
                  </option>

                  {cropOptions.map(
                    (option) => (
                      <option
                        key={
                          option.value
                        }
                        value={
                          option.value
                        }
                      >
                        {
                          option.label
                        }
                      </option>
                    )
                  )}
                </select>
              </div>
            </div>

            {/* Area */}
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs font-medium uppercase tracking-wider text-slate-400">
                {t("detectedArea")}
              </p>

              <div className="mt-2 flex items-end gap-2">
                <span className="text-3xl font-semibold text-slate-900">
                  {areaAcres > 0
                    ? areaAcres.toFixed(
                        2
                      )
                    : "—"}
                </span>

                <span className="mb-1 text-sm text-slate-500">
                  {t("acres")}
                </span>
              </div>

              {center && (
                <p className="mt-2 text-xs text-slate-500">
                  {t("center")}:{" "}
                  {center[0].toFixed(
                    5
                  )}
                  ,{" "}
                  {center[1].toFixed(
                    5
                  )}
                </p>
              )}
            </div>

            {/* Save */}
            <button
              type="button"
              onClick={
                handleSave
              }
              disabled={
                saving ||
                !farmName.trim() ||
                !boundary ||
                !center ||
                areaAcres <= 0
              }
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-600 px-4 py-3 text-sm font-medium text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400"
            >
              <Check size={18} />

              {saving
                ? "Saving..."
                : t("saveFarm")}
            </button>

            {/* Success */}
            {saved && (
              <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
                {t("farmSaved")}
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
                {error}
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}