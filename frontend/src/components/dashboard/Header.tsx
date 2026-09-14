"use client";

import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  Bell,
  Check,
  ChevronDown,
  Globe,
  LogOut,
  UserCircle,
} from "lucide-react";

import { useRouter } from "next/navigation";

import { useFarmStore } from "@/store/farmStore";

import {
  Language,
  useLanguage,
} from "@/context/LanguageContext";

import {
  getCurrentUserDetails,
  logoutUser,
} from "@/lib/auth";

import { BackendUser } from "@/lib/auth";

interface NotificationItem {
  id: number;

  type:
    | "weather"
    | "health"
    | "fertilizer";

  titleKey:
    | "weatherAlert"
    | "farmHealthNotification"
    | "fertilizerReminder";

  messageKey:
    | "weatherMessage"
    | "farmHealthMessage"
    | "fertilizerMessage";

  unread: boolean;
}

export default function Header() {
  const router = useRouter();

  const {
    language,
    setLanguage,
    t,
  } = useLanguage();

  const farms = useFarmStore(
    (state) => state.farms
  );

  const selectedFarmId =
    useFarmStore(
      (state) =>
        state.selectedFarmId
    );

  const selectedFarm = farms.find(
    (farm) =>
      farm.id === selectedFarmId
  );

  const [
    user,
    setUser,
  ] = useState<BackendUser | null>(
    null
  );

  const [
    userLoading,
    setUserLoading,
  ] = useState(true);

  const [
    notificationOpen,
    setNotificationOpen,
  ] = useState(false);

  const [
    languageOpen,
    setLanguageOpen,
  ] = useState(false);

  const [
    profileOpen,
    setProfileOpen,
  ] = useState(false);

  const [
    notifications,
    setNotifications,
  ] = useState<NotificationItem[]>([
    {
      id: 1,
      type: "weather",
      titleKey:
        "weatherAlert",
      messageKey:
        "weatherMessage",
      unread: true,
    },
    {
      id: 2,
      type: "health",
      titleKey:
        "farmHealthNotification",
      messageKey:
        "farmHealthMessage",
      unread: true,
    },
    {
      id: 3,
      type: "fertilizer",
      titleKey:
        "fertilizerReminder",
      messageKey:
        "fertilizerMessage",
      unread: true,
    },
  ]);

  const notificationRef =
    useRef<HTMLDivElement>(null);

  const languageRef =
    useRef<HTMLDivElement>(null);

  const profileRef =
    useRef<HTMLDivElement>(null);

  /*
   * Load the authenticated farmer
   * from the backend.
   */
  useEffect(() => {
    let mounted = true;

    const loadUser = async () => {
      try {
        const currentUser =
          await getCurrentUserDetails();

        if (mounted) {
          setUser(currentUser);
        }
      } catch (error) {
        console.error(
          "Failed to load user:",
          error
        );
      } finally {
        if (mounted) {
          setUserLoading(false);
        }
      }
    };

    loadUser();

    return () => {
      mounted = false;
    };
  }, []);

  /*
   * Close dropdowns when clicking
   * outside them.
   */
  useEffect(() => {
    const handleClickOutside = (
      event: MouseEvent
    ) => {
      const target =
        event.target as Node;

      if (
        notificationRef.current &&
        !notificationRef.current.contains(
          target
        )
      ) {
        setNotificationOpen(false);
      }

      if (
        languageRef.current &&
        !languageRef.current.contains(
          target
        )
      ) {
        setLanguageOpen(false);
      }

      if (
        profileRef.current &&
        !profileRef.current.contains(
          target
        )
      ) {
        setProfileOpen(false);
      }
    };

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
    };
  }, []);

  const unreadCount =
    notifications.filter(
      (notification) =>
        notification.unread
    ).length;

  const changeLanguage = (
    newLanguage: Language
  ) => {
    setLanguage(newLanguage);
    setLanguageOpen(false);
  };

  const markAllAsRead = () => {
    setNotifications((current) =>
      current.map(
        (notification) => ({
          ...notification,
          unread: false,
        })
      )
    );
  };

  const markNotificationAsRead = (
    id: number
  ) => {
    setNotifications((current) =>
      current.map(
        (notification) =>
          notification.id === id
            ? {
                ...notification,
                unread: false,
              }
            : notification
      )
    );
  };

  const handleLogout = () => {
    logoutUser();

    setProfileOpen(false);

    router.replace("/login");
  };

  const getNotificationIcon = (
    type: NotificationItem["type"]
  ) => {
    switch (type) {
      case "weather":
        return "🌧️";

      case "health":
        return "🌱";

      case "fertilizer":
        return "🧪";

      default:
        return "🔔";
    }
  };

  const getLanguageName = (
    value: Language
  ) => {
    switch (value) {
      case "hi":
        return "हिन्दी";

      case "bn":
        return "বাংলা";

      case "en":
      default:
        return "English";
    }
  };

  const getInitials = (
    name: string
  ) => {
    const parts =
      name.trim().split(/\s+/);

    if (parts.length === 0) {
      return "F";
    }

    if (parts.length === 1) {
      return parts[0]
        .slice(0, 1)
        .toUpperCase();
    }

    return (
      parts[0].slice(0, 1) +
      parts[parts.length - 1].slice(
        0,
        1
      )
    ).toUpperCase();
  };

  const farmerName =
    user?.name ||
    t("farmer");

  const farmerInitials =
    user?.name
      ? getInitials(user.name)
      : "F";

  return (
    <header className="sticky top-0 z-50 flex h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-6 backdrop-blur">
      {/* Current Farm */}
      <div>
        <p className="text-sm text-slate-500">
          {t("currentFarm")}
        </p>

        <button
          type="button"
          className="flex items-center gap-1 font-medium text-slate-900"
        >
          {selectedFarm?.name ||
            t("noFarmSelected")}

          <ChevronDown size={16} />
        </button>
      </div>

      <div className="flex items-center gap-3">
        {/* Language Selector */}
        <div
          ref={languageRef}
          className="relative"
        >
          <button
            type="button"
            onClick={() =>
              setLanguageOpen(
                (current) =>
                  !current
              )
            }
            className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-50"
            title={t("language")}
            aria-label={t("language")}
          >
            <Globe size={17} />

            <span className="hidden sm:inline">
              {getLanguageName(
                language
              )}
            </span>

            <ChevronDown size={14} />
          </button>

          {languageOpen && (
            <div className="absolute right-0 top-12 z-[100] w-44 overflow-hidden rounded-xl border border-slate-200 bg-white p-1 shadow-xl">
              <p className="px-3 py-2 text-xs font-medium uppercase tracking-wider text-slate-400">
                {t("language")}
              </p>

              {(
                [
                  ["en", "English"],
                  ["hi", "हिन्दी"],
                  ["bn", "বাংলা"],
                ] as const
              ).map(
                ([value, label]) => (
                  <button
                    type="button"
                    key={value}
                    onClick={() =>
                      changeLanguage(
                        value
                      )
                    }
                    className={`flex w-full items-center justify-between rounded-lg px-3 py-2.5 text-sm transition ${
                      language === value
                        ? "bg-emerald-50 font-medium text-emerald-700"
                        : "text-slate-600 hover:bg-slate-50"
                    }`}
                  >
                    <span>
                      {label}
                    </span>

                    {language ===
                      value && (
                      <Check
                        size={15}
                      />
                    )}
                  </button>
                )
              )}
            </div>
          )}
        </div>

        {/* Notifications */}
        <div
          ref={notificationRef}
          className="relative"
        >
          <button
            type="button"
            onClick={() =>
              setNotificationOpen(
                (current) =>
                  !current
              )
            }
            className="relative rounded-xl p-2.5 text-slate-500 transition hover:bg-slate-100 hover:text-slate-700"
            title={t(
              "notifications"
            )}
            aria-label={t(
              "notifications"
            )}
          >
            <Bell size={20} />

            {unreadCount > 0 && (
              <span className="absolute right-1 top-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-emerald-500 px-1 text-[9px] font-bold text-white">
                {unreadCount}
              </span>
            )}
          </button>

          {notificationOpen && (
            <div className="absolute right-0 top-12 z-[100] w-[360px] overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl">
              {/* Popup Header */}
              <div className="flex items-center justify-between border-b border-slate-100 px-4 py-3">
                <div>
                  <h3 className="font-semibold text-slate-900">
                    {t(
                      "notifications"
                    )}
                  </h3>

                  <p className="mt-0.5 text-xs text-slate-400">
                    {unreadCount}{" "}
                    {t("unread")}
                  </p>
                </div>

                {unreadCount >
                  0 && (
                  <button
                    type="button"
                    onClick={
                      markAllAsRead
                    }
                    className="text-xs font-medium text-emerald-600 hover:text-emerald-700"
                  >
                    {t(
                      "markAllRead"
                    )}
                  </button>
                )}
              </div>

              {/* Notification List */}
              <div className="max-h-[360px] overflow-y-auto">
                {notifications.length ===
                0 ? (
                  <div className="px-6 py-10 text-center">
                    <Bell
                      size={28}
                      className="mx-auto text-slate-300"
                    />

                    <p className="mt-3 text-sm text-slate-500">
                      {t(
                        "noNotifications"
                      )}
                    </p>
                  </div>
                ) : (
                  notifications.map(
                    (
                      notification
                    ) => (
                      <button
                        type="button"
                        key={
                          notification.id
                        }
                        onClick={() =>
                          markNotificationAsRead(
                            notification.id
                          )
                        }
                        className={`flex w-full gap-3 border-b border-slate-100 px-4 py-4 text-left transition hover:bg-slate-50 ${
                          notification.unread
                            ? "bg-emerald-50/40"
                            : "bg-white"
                        }`}
                      >
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-lg shadow-sm ring-1 ring-slate-100">
                          {getNotificationIcon(
                            notification.type
                          )}
                        </div>

                        <div className="min-w-0 flex-1">
                          <div className="flex items-start justify-between gap-2">
                            <p className="text-sm font-semibold text-slate-800">
                              {t(
                                notification.titleKey
                              )}
                            </p>

                            {notification.unread && (
                              <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-emerald-500" />
                            )}
                          </div>

                          <p className="mt-1 text-xs leading-5 text-slate-500">
                            {t(
                              notification.messageKey
                            )}
                          </p>
                        </div>
                      </button>
                    )
                  )
                )}
              </div>

              {/* Footer */}
              <div className="border-t border-slate-100 px-4 py-3">
                <button
                  type="button"
                  onClick={
                    markAllAsRead
                  }
                  className="flex w-full items-center justify-center gap-2 rounded-lg bg-slate-50 py-2 text-xs font-medium text-slate-600 transition hover:bg-emerald-50 hover:text-emerald-700"
                >
                  <Check
                    size={14}
                  />

                  {t(
                    "markAllRead"
                  )}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* User / Profile */}
        <div
          ref={profileRef}
          className="relative"
        >
          <button
            type="button"
            onClick={() =>
              setProfileOpen(
                (current) =>
                  !current
              )
            }
            className="flex items-center gap-3 rounded-xl px-2 py-1.5 transition hover:bg-slate-50"
            aria-label="Open profile menu"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-emerald-100 text-sm font-semibold text-emerald-700">
              {farmerInitials}
            </div>

            <div className="hidden text-left sm:block">
              <p className="max-w-[140px] truncate text-sm font-medium text-slate-900">
                {userLoading
                  ? "Loading..."
                  : farmerName}
              </p>

              <p className="text-xs text-slate-500">
                {t("farmOwner")}
              </p>
            </div>

            <ChevronDown
              size={15}
              className="hidden text-slate-400 sm:block"
            />
          </button>

          {profileOpen && (
            <div className="absolute right-0 top-14 z-[100] w-64 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl">
              {/* Profile information */}
              <div className="border-b border-slate-100 px-4 py-4">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-100 text-sm font-semibold text-emerald-700">
                    {farmerInitials}
                  </div>

                  <div className="min-w-0">
                    <p className="truncate text-sm font-semibold text-slate-900">
                      {farmerName}
                    </p>

                    <p className="truncate text-xs text-slate-500">
                      {user?.email ||
                        ""}
                    </p>
                  </div>
                </div>

                {user && (
                  <div className="mt-3 rounded-xl bg-slate-50 p-3">
                    <p className="text-xs text-slate-500">
                      {user.district},{" "}
                      {user.state}
                    </p>

                    <p className="mt-1 text-xs text-slate-400">
                      {user.area}
                    </p>
                  </div>
                )}
              </div>

              {/* Profile actions */}
              <div className="p-1">
                <button
                  type="button"
                  className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-slate-600 transition hover:bg-slate-50"
                >
                  <UserCircle
                    size={17}
                  />

                  {t("settings")}
                </button>

                <button
                  type="button"
                  onClick={
                    handleLogout
                  }
                  className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-red-600 transition hover:bg-red-50"
                >
                  <LogOut
                    size={17}
                  />

                  Logout
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}