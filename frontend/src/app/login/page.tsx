
"use client";

import {
  FormEvent,
  useState,
} from "react";

import Link from "next/link";

import {
  ArrowLeft,
  Eye,
  EyeOff,
} from "lucide-react";

import { useRouter } from "next/navigation";

import {
  loginUser,
} from "@/lib/auth";

import { useLanguage } from "@/context/LanguageContext";

export default function LoginPage() {
  const router = useRouter();

  const {
    language,
    setLanguage,
  } = useLanguage();

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [registered, setRegistered] =
    useState(false);

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    setError("");

    if (
      !email.trim() ||
      !password
    ) {
      setError(
        "Please enter your email and password."
      );

      return;
    }

    try {
      setLoading(true);

      const success =
        await loginUser(
          email,
          password
        );

      if (!success) {
        setError(
          "Account not found or password is incorrect."
        );

        return;
      }

      router.push(
        "/dashboard"
      );
    } catch (error) {
      console.error(
        "Login failed:",
        error
      );

      setError(
        "Unable to connect to the server. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto flex min-h-screen max-w-md flex-col px-6 py-8">
        <div className="flex items-center justify-between">
          <Link
            href="/"
            className="flex items-center gap-2 text-sm text-slate-500 transition hover:text-emerald-600"
          >
            <ArrowLeft size={16} />

            Home
          </Link>

          <LanguageSwitcher
            language={language}
            setLanguage={setLanguage}
          />
        </div>

        <div className="my-auto py-12">
          <div className="mb-8 text-center">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-600 text-2xl shadow-sm">
              🌾
            </div>

            <h1 className="mt-5 text-2xl font-semibold text-slate-900">
              Welcome back
            </h1>

            <p className="mt-2 text-sm text-slate-500">
              Sign in to your KrishiMap AI workspace.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
          >
            {registered && (
              <div className="mb-5 rounded-xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
                Account created successfully. Please log in.
              </div>
            )}

            {error && (
              <div className="mb-5 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600">
                {error}
              </div>
            )}

            <label className="text-sm font-medium text-slate-700">
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(
                  event.target.value
                )
              }
              placeholder="you@example.com"
              autoComplete="email"
              className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
            />

            <div className="mt-5 flex items-center justify-between">
              <label className="text-sm font-medium text-slate-700">
                Password
              </label>

              <Link
                href="/forgot-password"
                className="text-xs font-medium text-emerald-600 transition hover:text-emerald-700"
              >
                Forgot password?
              </Link>
            </div>

            <div className="relative mt-2">
              <input
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                value={password}
                onChange={(event) =>
                  setPassword(
                    event.target.value
                  )
                }
                placeholder="••••••••"
                autoComplete="current-password"
                className="w-full rounded-xl border border-slate-200 px-4 py-3 pr-11 text-sm outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
              />

              <button
                type="button"
                onClick={() =>
                  setShowPassword(
                    (current) =>
                      !current
                  )
                }
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 transition hover:text-slate-600"
                aria-label={
                  showPassword
                    ? "Hide password"
                    : "Show password"
                }
              >
                {showPassword ? (
                  <EyeOff size={18} />
                ) : (
                  <Eye size={18} />
                )}
              </button>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-6 w-full rounded-xl bg-emerald-600 px-4 py-3.5 text-sm font-semibold text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              {loading
                ? "Signing in..."
                : "Login"}
            </button>

            <p className="mt-6 text-center text-sm text-slate-500">
              Don't have an account?{" "}

              <Link
                href="/register"
                className="font-medium text-emerald-600 transition hover:text-emerald-700"
              >
                Sign up
              </Link>
            </p>
          </form>
        </div>
      </div>
    </main>
  );
}

function LanguageSwitcher({
  language,
  setLanguage,
}: {
  language:
    | "en"
    | "hi"
    | "bn";

  setLanguage: (
    language:
      | "en"
      | "hi"
      | "bn"
  ) => void;
}) {
  return (
    <div className="flex rounded-lg border border-slate-200 bg-white p-1">
      {[
        ["en", "EN"],
        ["hi", "हि"],
        ["bn", "বাং"],
      ].map(
        ([value, label]) => (
          <button
            type="button"
            key={value}
            onClick={() =>
              setLanguage(
                value as
                  | "en"
                  | "hi"
                  | "bn"
              )
            }
            className={`rounded-md px-2.5 py-1 text-xs transition ${
              language === value
                ? "bg-emerald-600 text-white"
                : "text-slate-500 hover:text-slate-700"
            }`}
          >
            {label}
          </button>
        )
      )}
    </div>
  );
}