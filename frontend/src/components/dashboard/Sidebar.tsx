"use client";

import Link from "next/link";

import {
  CalendarDays,
  LayoutDashboard,
  Map,
  Settings,
  Sprout,
  Plus,
} from "lucide-react";

import { useFarmStore } from "@/store/farmStore";

import { useLanguage } from "@/context/LanguageContext";

const navigation = [
  {
    key: "dashboard" as const,
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    key: "farmAnalysis" as const,
    href: "/dashboard/analysis",
    icon: Sprout,
  },
  {
    key: "farmCalendar" as const,
    href: "/dashboard/calendar",
    icon: CalendarDays,
  },
];

export default function Sidebar() {
  const { t } =
    useLanguage();

  const farms = useFarmStore(
    (state) => state.farms
  );

  const selectedFarmId =
    useFarmStore(
      (state) =>
        state.selectedFarmId
    );

  const selectFarm =
    useFarmStore(
      (state) =>
        state.selectFarm
    );

  return (
    <aside className="fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-slate-200 bg-white">
      {/* Logo */}
      <div className="flex h-16 items-center gap-3 border-b border-slate-200 px-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-600 text-lg">
          🌾
        </div>

        <div>
          <h1 className="font-semibold text-slate-900">
            {t("appName")}
          </h1>

          <p className="text-xs text-slate-500">
            {t("tagline")}
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="space-y-1 p-4">
        <p className="mb-3 px-3 text-xs font-medium uppercase tracking-wider text-slate-400">
          {t("workspace")}
        </p>

        {navigation.map(
          (item) => {
            const Icon =
              item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-slate-600 transition hover:bg-emerald-50 hover:text-emerald-700"
              >
                <Icon size={18} />

                {t(item.key)}
              </Link>
            );
          }
        )}
      </nav>

      {/* Farms */}
      <div className="px-4">
        <div className="mb-3 flex items-center justify-between px-3">
          <p className="text-xs font-medium uppercase tracking-wider text-slate-400">
            {t("myFarms")}
          </p>

          <Link
            href="/dashboard/farms"
            className="rounded-lg p-1 text-slate-400 hover:bg-emerald-50 hover:text-emerald-600"
            title={t("addFarm")}
            aria-label={t("addFarm")}
          >
            <Plus size={16} />
          </Link>
        </div>

        <div className="space-y-1">
          {farms.map(
            (farm) => {
              const active =
                selectedFarmId ===
                farm.id;

              return (
                <button
                  type="button"
                  key={farm.id}
                  onClick={() =>
                    selectFarm(
                      farm.id
                    )
                  }
                  className={`flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm transition ${
                    active
                      ? "bg-emerald-50 text-emerald-700"
                      : "text-slate-600 hover:bg-slate-50"
                  }`}
                >
                  <span
                    className={`h-2.5 w-2.5 rounded-full ${
                      active
                        ? "bg-emerald-500"
                        : "bg-slate-300"
                    }`}
                  />

                  <span className="min-w-0 flex-1">
                    <span className="block truncate font-medium">
                      {farm.name}
                    </span>

                    <span className="block text-xs text-slate-400">
                      {farm.areaAcres.toFixed(
                        2
                      )}{" "}
                      {t("acres")}
                    </span>
                  </span>
                </button>
              );
            }
          )}

          {/* No farms */}
          {farms.length ===
            0 && (
            <Link
              href="/dashboard/farms"
              className="block rounded-xl border border-dashed border-slate-200 p-4 text-center transition hover:border-emerald-200 hover:bg-emerald-50"
            >
              <Map
                size={20}
                className="mx-auto text-slate-300"
              />

              <p className="mt-2 text-xs font-medium text-slate-500">
                {t(
                  "addFirstFarm"
                )}
              </p>
            </Link>
          )}
        </div>
      </div>

      {/* Settings */}
      <div className="mt-auto p-4">
        <button
          type="button"
          className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-slate-600 hover:bg-slate-100"
        >
          <Settings size={18} />

          {t("settings")}
        </button>
      </div>
    </aside>
  );
}