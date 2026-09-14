
"use client";

import Link from "next/link";
import {
  ArrowRight,
  Globe2,
  Map,
  Sprout,
  Sparkles,
} from "lucide-react";

import { useLanguage } from "@/context/LanguageContext";

export default function Home() {
  const { language, setLanguage } = useLanguage();

  const languages = [
    {
      value: "en" as const,
      label: "English",
    },
    {
      value: "hi" as const,
      label: "हिन्दी",
    },
    {
      value: "bn" as const,
      label: "বাংলা",
    },
  ];

  return (
    <main className="min-h-screen bg-white">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col px-6">
        {/* Minimal top section */}
        <header className="flex items-center justify-between py-6">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-600 text-xl shadow-sm">
              🌾
            </div>

            <div>
              <h1 className="text-lg font-semibold text-slate-900">
                KrishiMap AI
              </h1>

              <p className="text-xs text-slate-500">
                AI Farm Intelligence
              </p>
            </div>
          </div>

          {/* Language selector */}
          <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white p-1">
            <Globe2
              size={16}
              className="ml-2 text-slate-400"
            />

            {languages.map((item) => (
              <button
                key={item.value}
                onClick={() => setLanguage(item.value)}
                className={`rounded-lg px-3 py-1.5 text-xs font-medium transition ${
                  language === item.value
                    ? "bg-emerald-600 text-white"
                    : "text-slate-500 hover:bg-slate-100"
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </header>

        {/* Hero */}
        <section className="flex flex-1 items-center py-12">
          <div className="grid w-full items-center gap-16 lg:grid-cols-2">
            {/* Left */}
            <div>
              <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-medium text-emerald-700">
                <Sparkles size={14} />
                AI Farm Intelligence
              </div>

              <h2 className="max-w-2xl text-5xl font-semibold leading-[1.1] tracking-tight text-slate-900">
                Smarter farming,
                <span className="block text-emerald-600">
                  powered by AI.
                </span>
              </h2>

              <p className="mt-6 max-w-xl text-lg leading-8 text-slate-500">
                Manage your farms, understand field conditions,
                monitor weather, plan crops and get intelligent
                farming recommendations from one place.
              </p>

              <div className="mt-8 flex flex-wrap gap-3">
                <Link
                  href="/login"
                  className="flex items-center gap-2 rounded-xl bg-emerald-600 px-6 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-700"
                >
                  Login
                  <ArrowRight size={17} />
                </Link>

                <Link
                  href="/register"
                  className="rounded-xl border border-slate-200 bg-white px-6 py-3.5 text-sm font-semibold text-slate-700 transition hover:border-emerald-300 hover:bg-emerald-50 hover:text-emerald-700"
                >
                  Create account
                </Link>
              </div>

              <p className="mt-6 text-xs text-slate-400">
                Your farm intelligence workspace starts here.
              </p>
            </div>

            {/* Right visual */}
            <div className="relative">
              <div className="absolute -inset-6 rounded-[2rem] bg-emerald-50 blur-2xl" />

              <div className="relative overflow-hidden rounded-[2rem] border border-slate-200 bg-white p-5 shadow-xl">
                {/* Fake map preview */}
                <div className="relative h-[390px] overflow-hidden rounded-2xl bg-emerald-50">
                  <div className="absolute inset-0 opacity-40">
                    <div className="absolute left-[10%] top-[12%] h-32 w-40 rotate-12 rounded-[35%] border-2 border-emerald-300 bg-emerald-100" />

                    <div className="absolute right-[12%] top-[25%] h-36 w-44 -rotate-6 rounded-[40%] border-2 border-emerald-300 bg-green-100" />

                    <div className="absolute bottom-[12%] left-[22%] h-32 w-52 rotate-3 rounded-[35%] border-2 border-emerald-300 bg-emerald-100" />

                    <div className="absolute bottom-[18%] right-[12%] h-24 w-36 -rotate-12 rounded-[40%] border-2 border-emerald-300 bg-green-100" />
                  </div>

                  <div className="absolute left-1/2 top-1/2 flex -translate-x-1/2 -translate-y-1/2 flex-col items-center">
                    <div className="flex h-14 w-14 items-center justify-center rounded-full bg-emerald-600 text-2xl text-white shadow-lg ring-8 ring-white/60">
                      🌾
                    </div>

                    <div className="mt-3 rounded-xl bg-white px-4 py-2 shadow-lg">
                      <p className="text-xs font-semibold text-slate-800">
                        Your Farm
                      </p>

                      <p className="text-[10px] text-slate-400">
                        AI-powered monitoring
                      </p>
                    </div>
                  </div>

                  {/* Floating cards */}
                  <div className="absolute left-4 top-4 rounded-xl border border-white/80 bg-white/95 p-3 shadow-lg backdrop-blur">
                    <div className="flex items-center gap-2">
                      <Map
                        size={17}
                        className="text-emerald-600"
                      />

                      <div>
                        <p className="text-[10px] text-slate-400">
                          Farm Area
                        </p>

                        <p className="text-sm font-semibold text-slate-800">
                          GIS Ready
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="absolute bottom-4 right-4 rounded-xl border border-white/80 bg-white/95 p-3 shadow-lg backdrop-blur">
                    <div className="flex items-center gap-2">
                      <Sprout
                        size={17}
                        className="text-emerald-600"
                      />

                      <div>
                        <p className="text-[10px] text-slate-400">
                          Crop Intelligence
                        </p>

                        <p className="text-sm font-semibold text-slate-800">
                          AI Assisted
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <footer className="border-t border-slate-100 py-5 text-center text-xs text-slate-400">
          KrishiMap AI · AI Farm Intelligence
        </footer>
      </div>
    </main>
  );
}