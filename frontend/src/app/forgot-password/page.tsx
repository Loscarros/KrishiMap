
"use client";

import {
    FormEvent,
    useState,
} from "react";

import Link from "next/link";

import {
    ArrowLeft,
    Info,
} from "lucide-react";

export default function ForgotPasswordPage() {
    const [email, setEmail] =
        useState("");

    const [message, setMessage] =
        useState("");

    const [error, setError] =
        useState("");

    const handleSubmit = (
        event: FormEvent<HTMLFormElement>
    ) => {
        event.preventDefault();

        setMessage("");
        setError("");

        if (!email.trim()) {
            setError(
                "Please enter your email address."
            );

            return;
        }

        if (
            !email.includes("@") ||
            !email.includes(".")
        ) {
            setError(
                "Please enter a valid email address."
            );

            return;
        }

        setMessage(
            "Password reset is not configured yet. Your account is securely stored in the KrishiMap AI backend."
        );
    };

    return (
        <main className="min-h-screen bg-slate-50">
            <div className="mx-auto flex min-h-screen max-w-md flex-col px-6 py-8">
                <Link
                    href="/login"
                    className="flex items-center gap-2 text-sm text-slate-500 transition hover:text-emerald-600"
                >
                    <ArrowLeft size={16} />

                    Back to login
                </Link>

                <div className="my-auto py-12">
                    <div className="mb-8 text-center">
                        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-600 text-2xl shadow-sm">
                            🔐
                        </div>

                        <h1 className="mt-5 text-2xl font-semibold text-slate-900">
                            Forgot password?
                        </h1>

                        <p className="mt-2 text-sm leading-6 text-slate-500">
                            Enter the email associated with your KrishiMap AI account.
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

                        {message && (
                            <div className="mb-5 flex gap-3 rounded-xl border border-blue-100 bg-blue-50 px-4 py-3 text-sm text-blue-700">
                                <Info
                                    size={18}
                                    className="shrink-0"
                                />

                                <span>
                                    {message}
                                </span>
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

                        <button
                            type="submit"
                            className="mt-5 w-full rounded-xl bg-emerald-600 px-4 py-3.5 text-sm font-semibold text-white transition hover:bg-emerald-700"
                        >
                            Continue
                        </button>

                        <p className="mt-6 text-center text-sm text-slate-500">
                            Remember your password?{" "}

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