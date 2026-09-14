
"use client";

import {
  ReactNode,
  useEffect,
  useState,
} from "react";

import { useRouter } from "next/navigation";

import Sidebar from "@/components/dashboard/Sidebar";
import Header from "@/components/dashboard/Header";

import {
  clearToken,
  getCurrentUserDetails,
  isAuthenticated,
} from "@/lib/auth";

import { useFarmStore } from "@/store/farmStore";

export default function DashboardLayout({
  children,
}: {
  children: ReactNode;
}) {
  const router = useRouter();

  const loadFarms =
    useFarmStore(
      (state) => state.loadFarms
    );

  const farmsLoading =
    useFarmStore(
      (state) => state.loading
    );

  const [
    ready,
    setReady,
  ] = useState(false);

  useEffect(() => {
    let mounted = true;

    const validateSession =
      async () => {
        /*
         * First make sure a JWT exists.
         */
        if (!isAuthenticated()) {
          router.replace("/login");
          return;
        }

        /*
         * Validate the JWT against FastAPI.
         *
         * We do NOT trust only localStorage.
         */
        const user =
          await getCurrentUserDetails();

        if (!user) {
          clearToken();

          router.replace("/login");

          return;
        }

        /*
         * The farmer is authenticated.
         *
         * Now load the farms from PostgreSQL.
         *
         * This is what makes farms survive
         * browser refreshes.
         */
        await loadFarms();

        if (mounted) {
          setReady(true);
        }
      };

    validateSession();

    return () => {
      mounted = false;
    };
  }, [
    router,
    loadFarms,
  ]);

  if (!ready || farmsLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-600 text-xl">
            🌾
          </div>

          <p className="mt-3 text-sm text-slate-500">
            Loading KrishiMap AI...
          </p>

          <p className="mt-1 text-xs text-slate-400">
            Loading your farms...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />

      <div className="ml-64">
        <Header />

        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  );
}