
"use client";

import Link from "next/link";
import {
  ArrowUpRight,
  MapPin,
  Ruler,
  Sprout,
} from "lucide-react";

import { Farm } from "@/types/farm";
import { useLanguage } from "@/context/LanguageContext";

interface FarmCardProps {
  farm: Farm;
}

export default function FarmCard({
  farm,
}: FarmCardProps) {
  const { t } = useLanguage();

  const getLocalizedCrop = (
    crop?: string
  ) => {
    if (!crop) {
      return t("selectCrop");
    }

    const cropMap: Record<
      string,
      "rice" | "maize" | "wheat" | "potato" | "tomato" | "otherCrop"
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

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5">
      {/* Farm Header */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50 text-xl">
            🌾
          </div>

          <div>
            <h2 className="font-semibold text-slate-900">
              {farm.name}
            </h2>

            <p className="text-xs text-slate-500">
              {t("farmOwner")}
            </p>
          </div>
        </div>

        <Link
          href="/dashboard/farms"
          className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-50 hover:text-emerald-600"
          title={t("addFarm")}
          aria-label={t("addFarm")}
        >
          <ArrowUpRight size={18} />
        </Link>
      </div>

      {/* Farm Information */}
      <div className="mt-6 grid grid-cols-2 gap-3">
        <InfoItem
          icon={<Ruler size={16} />}
          label={t("detectedArea")}
          value={`${farm.areaAcres.toFixed(2)} ${t(
            "acres"
          )}`}
        />

        <InfoItem
          icon={<Sprout size={16} />}
          label={t("currentCrop")}
          value={getLocalizedCrop(
            farm.crop
          )}
        />

        <InfoItem
          icon={<MapPin size={16} />}
          label="Latitude"
          value={farm.latitude.toFixed(4)}
        />

        <InfoItem
          icon={<MapPin size={16} />}
          label="Longitude"
          value={farm.longitude.toFixed(4)}
        />
      </div>

      {/* GIS Status */}
      <div className="mt-4 rounded-xl bg-emerald-50 p-3">
        <p className="text-xs font-medium text-emerald-700">
          {t("farmBoundary")}
        </p>

        <p className="mt-1 text-xs text-emerald-600">
          {t("spatialOverview")}
        </p>
      </div>
    </section>
  );
}

function InfoItem({
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
      <div className="flex items-center gap-2 text-slate-400">
        {icon}

        <span className="text-xs">
          {label}
        </span>
      </div>

      <p className="mt-2 truncate text-sm font-medium text-slate-800">
        {value}
      </p>
    </div>
  );
}