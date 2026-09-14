"use client";

import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  CalendarDays,
  Check,
  ChevronLeft,
  ChevronRight,
  Clock3,
  Droplets,
  Leaf,
  Plus,
  Sprout,
  Wheat,
} from "lucide-react";

import type { LucideIcon } from "lucide-react";

import {
  addMonths,
  eachDayOfInterval,
  endOfMonth,
  format,
  isSameDay,
  startOfMonth,
  subMonths,
} from "date-fns";

import { useFarmStore } from "@/store/farmStore";

import {
  createFarmTask,
  getFarmTasks,
  updateFarmTask,
} from "@/lib/taskApi";

import { FarmTask } from "@/types/calendar";

import { useLanguage } from "@/context/LanguageContext";

/*
 * Reuse the exact translation-function type
 * from LanguageContext instead of widening it
 * to (key: string) => string.
 */
type Translate = ReturnType<typeof useLanguage>["t"];

type TaskStyle = {
  icon: LucideIcon;
  className: string;
};

function TaskBadge({
  task,
  compact = false,
}: {
  task: FarmTask;
  compact?: boolean;
}) {
  const { t } = useLanguage();

  const style = getTaskStyle(task.type);
  const Icon = style.icon;

  return (
    <div
      className={`flex items-center gap-1.5 rounded-lg border px-2 py-1 text-xs ${
        style.className
      } ${
        task.status === "completed"
          ? "opacity-50 line-through"
          : ""
      }`}
    >
      <Icon size={12} />

      {!compact && (
        <span className="truncate font-medium">
          {getTaskLabel(task.type, t)}
        </span>
      )}
    </div>
  );
}

function getTaskStyle(
  type: FarmTask["type"]
): TaskStyle {
  const styles: Record<
    FarmTask["type"],
    TaskStyle
  > = {
    irrigation: {
      icon: Droplets,
      className:
        "bg-blue-50 text-blue-700 border-blue-100",
    },

    fertilizer: {
      icon: Leaf,
      className:
        "bg-amber-50 text-amber-700 border-amber-100",
    },

    monitoring: {
      icon: Sprout,
      className:
        "bg-emerald-50 text-emerald-700 border-emerald-100",
    },

    harvest: {
      icon: Wheat,
      className:
        "bg-orange-50 text-orange-700 border-orange-100",
    },

    other: {
      icon: CalendarDays,
      className:
        "bg-slate-50 text-slate-700 border-slate-100",
    },
  };

  return styles[type];
}

function getTaskLabel(
  type: FarmTask["type"],
  t: Translate
) {
  switch (type) {
    case "irrigation":
      return t("irrigation");

    case "fertilizer":
      return t("fertilizer");

    case "monitoring":
      return t("monitoring");

    case "harvest":
      return t("harvest");

    case "other":
    default:
      return t("other");
  }
}

function getDateLocale(
  language: "en" | "hi" | "bn"
) {
  if (language === "hi") {
    return "hi-IN";
  }

  if (language === "bn") {
    return "bn-IN";
  }

  return "en-IN";
}

export default function CalendarPage() {
  const { language, t } = useLanguage();

  const farms = useFarmStore(
    (state) => state.farms
  );

  const selectedFarmId =
    useFarmStore(
      (state) => state.selectedFarmId
    );

  const selectedFarm = farms.find(
    (farm) =>
      farm.id === selectedFarmId
  );

  const locale = getDateLocale(language);

  const today = useMemo(
    () => new Date(),
    []
  );

  const [currentMonth, setCurrentMonth] =
    useState(
      startOfMonth(today)
    );

  const [selectedDate, setSelectedDate] =
    useState(today);

  const [tasks, setTasks] =
    useState<FarmTask[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState("");

  const [
    showAddTask,
    setShowAddTask,
  ] = useState(false);

  const [
    newTaskTitle,
    setNewTaskTitle,
  ] = useState("");

  const [
    newTaskType,
    setNewTaskType,
  ] = useState<FarmTask["type"]>(
    "other"
  );

  /*
   * Load tasks whenever the selected
   * farm changes.
   */
  useEffect(() => {
    if (!selectedFarmId) {
      setTasks([]);
      setLoading(false);
      return;
    }

    const farmId = selectedFarmId;

    let mounted = true;

    const loadTasks = async () => {
      try {
        setLoading(true);
        setError("");

        const farmTasks =
          await getFarmTasks(farmId);

        if (mounted) {
          setTasks(farmTasks);
        }
      } catch (error) {
        console.error(
          "Failed to load farm tasks:",
          error
        );

        if (mounted) {
          setError(
            "Unable to load farm activities."
          );

          setTasks([]);
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadTasks();

    return () => {
      mounted = false;
    };
  }, [selectedFarmId]);

  const days = useMemo(() => {
    return eachDayOfInterval({
      start: startOfMonth(
        currentMonth
      ),
      end: endOfMonth(
        currentMonth
      ),
    });
  }, [currentMonth]);

  const firstDayOffset =
    startOfMonth(
      currentMonth
    ).getDay();

  const selectedDayTasks =
    tasks.filter((task) =>
      isSameDay(
        new Date(
          `${task.date}T00:00:00`
        ),
        selectedDate
      )
    );

  const upcomingTasks = [...tasks]
    .filter(
      (task) =>
        task.status !== "completed"
    )
    .sort(
      (a, b) =>
        new Date(
          `${a.date}T00:00:00`
        ).getTime() -
        new Date(
          `${b.date}T00:00:00`
        ).getTime()
    )
    .slice(0, 5);

  const toggleTask = async (
    taskId: string
  ) => {
    if (!selectedFarmId) {
      return;
    }

    const currentTask =
      tasks.find(
        (task) =>
          task.id === taskId
      );

    if (!currentTask) {
      return;
    }

    const nextStatus =
      currentTask.status ===
      "completed"
        ? "pending"
        : "completed";

    try {
      setError("");

      const updatedTask =
        await updateFarmTask(
          selectedFarmId,
          taskId,
          {
            status: nextStatus,
          }
        );

      setTasks((current) =>
        current.map((task) =>
          task.id === taskId
            ? updatedTask
            : task
        )
      );
    } catch (error) {
      console.error(
        "Failed to update task:",
        error
      );

      setError(
        "Unable to update the activity."
      );
    }
  };

  const addTask = async () => {
    if (
      !selectedFarmId ||
      !newTaskTitle.trim()
    ) {
      return;
    }

    try {
      setSaving(true);
      setError("");

      const newTask =
        await createFarmTask(
          selectedFarmId,
          {
            title:
              newTaskTitle.trim(),

            description:
              "Added manually from the farm calendar.",

            date: format(
              selectedDate,
              "yyyy-MM-dd"
            ),

            type: newTaskType,

            status: "pending",
          }
        );

      setTasks((current) => [
        ...current,
        newTask,
      ]);

      setNewTaskTitle("");
      setNewTaskType("other");
      setShowAddTask(false);
    } catch (error) {
      console.error(
        "Failed to create task:",
        error
      );

      setError(
        "Unable to create the activity."
      );
    } finally {
      setSaving(false);
    }
  };

  const formatLongDate = (
    date: Date
  ) =>
    new Intl.DateTimeFormat(
      locale,
      {
        day: "2-digit",
        month: "long",
        year: "numeric",
      }
    ).format(date);

  const formatShortDate = (
    date: Date
  ) =>
    new Intl.DateTimeFormat(
      locale,
      {
        day: "2-digit",
        month: "short",
      }
    ).format(date);

  if (!selectedFarm) {
    return (
      <div className="flex min-h-[70vh] items-center justify-center">
        <div className="text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-600">
            <CalendarDays size={24} />
          </div>

          <h1 className="mt-4 text-xl font-semibold text-slate-900">
            {t("noFarmSelected")}
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            {t("addFirstFarm")}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700">
            <CalendarDays size={22} />
          </div>

          <div>
            <h1 className="text-2xl font-semibold text-slate-900">
              {t("farmCalendar")}
            </h1>

            <p className="mt-1 text-sm text-slate-500">
              {t("nextActivities")}{" "}
              <span className="font-medium text-slate-700">
                {selectedFarm.name}
              </span>
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={() =>
            setShowAddTask(true)
          }
          className="flex items-center justify-center gap-2 rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-emerald-700"
        >
          <Plus size={17} />

          {t("addActivity")}
        </button>
      </div>

      {/* Error */}

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Add Task */}

      {showAddTask && (
        <section className="rounded-2xl border border-emerald-200 bg-emerald-50/50 p-5">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-semibold text-slate-900">
                {t("addFarmTask")}
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                {t("selectedDate")}:{" "}
                {formatLongDate(
                  selectedDate
                )}
              </p>
            </div>

            <button
              type="button"
              onClick={() =>
                setShowAddTask(false)
              }
              className="text-sm text-slate-500 hover:text-slate-900"
            >
              {t("cancel")}
            </button>
          </div>

          <div className="mt-4 grid gap-3 md:grid-cols-[1fr_180px_auto]">
            <input
              value={newTaskTitle}
              onChange={(event) =>
                setNewTaskTitle(
                  event.target.value
                )
              }
              onKeyDown={(event) => {
                if (
                  event.key === "Enter" &&
                  !saving
                ) {
                  addTask();
                }
              }}
              placeholder={t(
                "addActivity"
              )}
              className="rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
            />

            <select
              value={newTaskType}
              onChange={(event) =>
                setNewTaskType(
                  event.target
                    .value as FarmTask["type"]
                )
              }
              className="rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-emerald-500"
            >
              <option value="irrigation">
                {t("irrigation")}
              </option>

              <option value="fertilizer">
                {t("fertilizer")}
              </option>

              <option value="monitoring">
                {t("monitoring")}
              </option>

              <option value="harvest">
                {t("harvest")}
              </option>

              <option value="other">
                {t("other")}
              </option>
            </select>

            <button
              type="button"
              onClick={addTask}
              disabled={
                saving ||
                !newTaskTitle.trim()
              }
              className="rounded-xl bg-emerald-600 px-5 py-3 text-sm font-medium text-white hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400"
            >
              {saving
                ? t("loading")
                : t("create")}
            </button>
          </div>
        </section>
      )}

      {/* Main */}

      <div className="grid gap-6 xl:grid-cols-[1fr_340px]">
        {/* Calendar */}

        <section className="rounded-2xl border border-slate-200 bg-white">
          <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
            <div>
              <h2 className="text-lg font-semibold text-slate-900">
                {new Intl.DateTimeFormat(
                  locale,
                  {
                    month: "long",
                    year: "numeric",
                  }
                ).format(
                  currentMonth
                )}
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                {t("selectDate")}
              </p>
            </div>

            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={() =>
                  setCurrentMonth(
                    subMonths(
                      currentMonth,
                      1
                    )
                  )
                }
                className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-900"
              >
                <ChevronLeft size={18} />
              </button>

              <button
                type="button"
                onClick={() => {
                  const now =
                    new Date();

                  setCurrentMonth(
                    startOfMonth(now)
                  );

                  setSelectedDate(now);
                }}
                className="rounded-lg px-3 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100"
              >
                {t("today")}
              </button>

              <button
                type="button"
                onClick={() =>
                  setCurrentMonth(
                    addMonths(
                      currentMonth,
                      1
                    )
                  )
                }
                className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-900"
              >
                <ChevronRight size={18} />
              </button>
            </div>
          </div>

          <div className="p-4">
            {/* Weekdays */}

            <div className="mb-2 grid grid-cols-7">
              {Array.from(
                { length: 7 },
                (_, index) =>
                  new Intl.DateTimeFormat(
                    locale,
                    {
                      weekday:
                        "short",
                    }
                  ).format(
                    new Date(
                      2024,
                      0,
                      7 + index
                    )
                  )
              ).map(
                (
                  day,
                  index
                ) => (
                  <div
                    key={`${day}-${index}`}
                    className="py-2 text-center text-xs font-medium uppercase tracking-wider text-slate-400"
                  >
                    {day}
                  </div>
                )
              )}
            </div>

            {/* Days */}

            <div className="grid grid-cols-7 overflow-hidden rounded-xl border border-slate-200">
              {Array.from({
                length:
                  firstDayOffset,
              }).map(
                (_, index) => (
                  <div
                    key={`empty-${index}`}
                    className="min-h-[105px] border-b border-r border-slate-100 bg-slate-50/40"
                  />
                )
              )}

              {days.map((day) => {
                const dayTasks =
                  tasks.filter(
                    (task) =>
                      isSameDay(
                        new Date(
                          `${task.date}T00:00:00`
                        ),
                        day
                      )
                  );

                const selected =
                  isSameDay(
                    day,
                    selectedDate
                  );

                const isToday =
                  isSameDay(
                    day,
                    today
                  );

                return (
                  <button
                    type="button"
                    key={day.toISOString()}
                    onClick={() => {
                      setSelectedDate(
                        day
                      );
                    }}
                    className={`min-h-[105px] border-b border-r border-slate-100 p-2 text-left align-top transition hover:bg-emerald-50/40 ${
                      selected
                        ? "bg-emerald-50/70 ring-2 ring-inset ring-emerald-400"
                        : "bg-white"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span
                        className={`flex h-7 w-7 items-center justify-center rounded-full text-xs font-medium ${
                          isToday
                            ? "bg-emerald-600 text-white"
                            : selected
                            ? "bg-emerald-100 text-emerald-700"
                            : "text-slate-600"
                        }`}
                      >
                        {format(
                          day,
                          "d"
                        )}
                      </span>

                      {dayTasks.length >
                        0 && (
                        <span className="text-[10px] text-slate-400">
                          {
                            dayTasks.length
                          }
                        </span>
                      )}
                    </div>

                    <div className="mt-2 space-y-1">
                      {dayTasks
                        .slice(0, 2)
                        .map(
                          (task) => (
                            <TaskBadge
                              key={
                                task.id
                              }
                              task={
                                task
                              }
                            />
                          )
                        )}

                      {dayTasks.length >
                        2 && (
                        <p className="px-1 text-[10px] text-slate-400">
                          +
                          {dayTasks.length -
                            2}{" "}
                          more
                        </p>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </section>

        {/* Side Panel */}

        <div className="space-y-6">
          {/* Selected Day */}

          <section className="rounded-2xl border border-slate-200 bg-white p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-medium uppercase tracking-wider text-slate-400">
                  {t("selectedDate")}
                </p>

                <h2 className="mt-1 text-lg font-semibold text-slate-900">
                  {formatLongDate(
                    selectedDate
                  )}
                </h2>
              </div>

              <button
                type="button"
                onClick={() =>
                  setShowAddTask(true)
                }
                className="rounded-lg bg-emerald-50 p-2 text-emerald-600 hover:bg-emerald-100"
                title={t(
                  "addActivity"
                )}
                aria-label={t(
                  "addActivity"
                )}
              >
                <Plus size={17} />
              </button>
            </div>

            <div className="mt-5 space-y-3">
              {loading ? (
                <div className="rounded-xl border border-dashed border-slate-200 p-5 text-center">
                  <div className="mx-auto h-5 w-5 animate-spin rounded-full border-2 border-slate-200 border-t-emerald-600" />

                  <p className="mt-3 text-sm text-slate-500">
                    {t("loading")}
                  </p>
                </div>
              ) : selectedDayTasks.length ===
                0 ? (
                <div className="rounded-xl border border-dashed border-slate-200 p-5 text-center">
                  <Clock3
                    size={22}
                    className="mx-auto text-slate-300"
                  />

                  <p className="mt-2 text-sm font-medium text-slate-600">
                    {t(
                      "noTasksScheduled"
                    )}
                  </p>

                  <p className="mt-1 text-xs text-slate-400">
                    {t("addActivity")}
                  </p>
                </div>
              ) : (
                selectedDayTasks.map(
                  (task) => {
                    const style =
                      getTaskStyle(
                        task.type
                      );

                    const Icon =
                      style.icon;

                    return (
                      <div
                        key={
                          task.id
                        }
                        className="rounded-xl border border-slate-200 p-4"
                      >
                        <div className="flex items-start gap-3">
                          <div
                            className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${style.className}`}
                          >
                            <Icon
                              size={17}
                            />
                          </div>

                          <div className="min-w-0 flex-1">
                            <div className="flex items-start justify-between gap-2">
                              <div>
                                <h3
                                  className={`text-sm font-semibold text-slate-900 ${
                                    task.status ===
                                    "completed"
                                      ? "line-through opacity-50"
                                      : ""
                                  }`}
                                >
                                  {
                                    task.title
                                  }
                                </h3>

                                <p className="mt-1 text-xs text-slate-500">
                                  {
                                    task.description
                                  }
                                </p>
                              </div>

                              <button
                                type="button"
                                onClick={() =>
                                  toggleTask(
                                    task.id
                                  )
                                }
                                className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-lg border transition ${
                                  task.status ===
                                  "completed"
                                    ? "border-emerald-200 bg-emerald-50 text-emerald-600"
                                    : "border-slate-200 text-slate-400 hover:border-emerald-200 hover:text-emerald-600"
                                }`}
                                title={t(
                                  "completed"
                                )}
                                aria-label={t(
                                  "completed"
                                )}
                              >
                                <Check
                                  size={
                                    15
                                  }
                                />
                              </button>
                            </div>

                            <div className="mt-3">
                              <span
                                className={`rounded-full border px-2 py-1 text-[10px] font-medium ${style.className}`}
                              >
                                {getTaskLabel(
                                  task.type,
                                  t
                                )}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  }
                )
              )}
            </div>
          </section>

          {/* Upcoming */}

          <section className="rounded-2xl border border-slate-200 bg-white p-5">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-semibold text-slate-900">
                  {t(
                    "upcomingTasks"
                  )}
                </h2>

                <p className="mt-1 text-xs text-slate-500">
                  {t(
                    "nextActivities"
                  )}
                </p>
              </div>

              <CalendarDays
                size={18}
                className="text-emerald-600"
              />
            </div>

            <div className="mt-5 space-y-3">
              {upcomingTasks.length ===
              0 ? (
                <div className="rounded-xl border border-dashed border-slate-200 p-4 text-center">
                  <p className="text-xs text-slate-400">
                    {t(
                      "noTasksScheduled"
                    )}
                  </p>
                </div>
              ) : (
                upcomingTasks.map(
                  (task) => {
                    const style =
                      getTaskStyle(
                        task.type
                      );

                    const Icon =
                      style.icon;

                    return (
                      <button
                        type="button"
                        key={
                          task.id
                        }
                        onClick={() => {
                          const date =
                            new Date(
                              `${task.date}T00:00:00`
                            );

                          setSelectedDate(
                            date
                          );

                          setCurrentMonth(
                            startOfMonth(
                              date
                            )
                          );
                        }}
                        className="flex w-full items-center gap-3 rounded-xl border border-slate-100 p-3 text-left transition hover:border-emerald-200 hover:bg-emerald-50/40"
                      >
                        <div
                          className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${style.className}`}
                        >
                          <Icon
                            size={16}
                          />
                        </div>

                        <div className="min-w-0 flex-1">
                          <p className="truncate text-sm font-medium text-slate-800">
                            {
                              task.title
                            }
                          </p>

                          <p className="mt-0.5 text-xs text-slate-400">
                            {formatShortDate(
                              new Date(
                                `${task.date}T00:00:00`
                              )
                            )}
                          </p>
                        </div>
                      </button>
                    );
                  }
                )
              )}
            </div>
          </section>
        </div>
      </div>

      {/* Legend */}

      <section className="flex flex-wrap items-center gap-3 rounded-2xl border border-slate-200 bg-white px-5 py-4">
        <span className="mr-2 text-xs font-medium uppercase tracking-wider text-slate-400">
          {t("taskTypes")}
        </span>

        {(
          [
            "irrigation",
            "fertilizer",
            "monitoring",
            "harvest",
            "other",
          ] as FarmTask["type"][]
        ).map((type) => {
          const style =
            getTaskStyle(type);

          const Icon =
            style.icon;

          return (
            <div
              key={type}
              className={`flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-medium ${style.className}`}
            >
              <Icon size={13} />

              {getTaskLabel(
                type,
                t
              )}
            </div>
          );
        })}
      </section>
    </div>
  );
}