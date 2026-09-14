
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

import { api } from "@/lib/api";
import { useLanguage } from "@/context/LanguageContext";

export default function RegisterPage() {
  const router = useRouter();

  const {
    language,
    setLanguage,
  } = useLanguage();

  const [name, setName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [state, setState] =
    useState("");

  const [district, setDistrict] =
    useState("");

  const [area, setArea] =
    useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    setError("");

    if (
      !name.trim() ||
      !email.trim() ||
      !password ||
      !state.trim() ||
      !district.trim() ||
      !area.trim()
    ) {
      setError(
        "Please fill in all the fields."
      );

      return;
    }

    if (password.length < 8) {
      setError(
        "Password must contain at least 8 characters."
      );

      return;
    }

    try {
      setLoading(true);

      await api.post(
        "/auth/register",
        {
          name: name.trim(),
          email:
            email.trim().toLowerCase(),
          password,
          state: state.trim(),
          district: district.trim(),
          area: area.trim(),
        }
      );

      router.push(
        `/login?registered=true`
      );
    } catch (error: any) {
      console.error(
        "Registration failed:",
        error
      );

      const detail =
        error?.response?.data?.detail;

      if (
        typeof detail === "string"
      ) {
        setError(detail);
      } else {
        setError(
          "Unable to create your account. Please make sure the backend is running."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-md px-6 py-8">
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

        <div className="py-10">
          <div className="mb-7 text-center">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-600 text-2xl shadow-sm">
              🌾
            </div>

            <h1 className="mt-5 text-2xl font-semibold text-slate-900">
              Create your farm account
            </h1>

            <p className="mt-2 text-sm text-slate-500">
              Tell us where your farm is located.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
          >
            {error && (
              <div className="mb-5 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600">
                {error}
              </div>
            )}

            <Field
              label="Full name"
              value={name}
              onChange={setName}
              placeholder="Your name"
            />

            <Field
              label="Email"
              type="email"
              value={email}
              onChange={setEmail}
              placeholder="you@example.com"
            />

            <div className="mt-5">
              <label className="text-sm font-medium text-slate-700">
                Password
              </label>

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
                  placeholder="At least 8 characters"
                  autoComplete="new-password"
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

              <p className="mt-2 text-xs text-slate-400">
                Use at least 8 characters.
              </p>
            </div>

            <div className="my-6 border-t border-slate-100" />

            <p className="mb-4 text-xs font-semibold uppercase tracking-wider text-emerald-600">
              Farm location
            </p>

            <div className="grid gap-4 sm:grid-cols-2">
              <Field
                label="State"
                value={state}
                onChange={setState}
                placeholder="Odisha"
              />

              <Field
                label="District"
                value={district}
                onChange={setDistrict}
                placeholder="Khordha"
              />
            </div>

            <div className="mt-4">
              <Field
                label="Area / Village"
                value={area}
                onChange={setArea}
                placeholder="Bhubaneswar / Village name"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-6 w-full rounded-xl bg-emerald-600 px-4 py-3.5 text-sm font-semibold text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              {loading
                ? "Creating account..."
                : "Create account"}
            </button>

            <p className="mt-6 text-center text-sm text-slate-500">
              Already have an account?{" "}

              <Link
                href="/login"
                className="font-medium text-emerald-600 transition hover:text-emerald-700"
              >
                Login
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

function Field({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (
    value: string
  ) => void;
  placeholder: string;
  type?: string;
}) {
  return (
    <div className="mt-4 first:mt-0">
      <label className="text-sm font-medium text-slate-700">
        {label}
      </label>

      <input
        type={type}
        value={value}
        onChange={(event) =>
          onChange(
            event.target.value
          )
        }
        placeholder={placeholder}
        autoComplete={
          type === "email"
            ? "email"
            : "off"
        }
        className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
      />
    </div>
  );
}