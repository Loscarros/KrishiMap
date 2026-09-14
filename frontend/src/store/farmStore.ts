
import { create } from "zustand";

import { Farm } from "@/types/farm";
import {
  getFarms,
  createFarm,
} from "@/lib/farmApi";

interface FarmStore {
  farms: Farm[];

  selectedFarmId: string | null;

  loading: boolean;

  error: string | null;

  /**
   * Replace the current farm list with
   * farms loaded from PostgreSQL.
   */
  setFarms: (farms: Farm[]) => void;

  /**
   * Load farms belonging to the
   * authenticated farmer from FastAPI.
   */
  loadFarms: () => Promise<void>;

  /**
   * Add a farm that has already been
   * successfully created in PostgreSQL.
   */
  addFarm: (farm: Farm) => void;

  selectFarm: (farmId: string) => void;

  removeFarm: (farmId: string) => void;

  clearFarms: () => void;
}

export const useFarmStore =
  create<FarmStore>((set, get) => ({
    farms: [],

    selectedFarmId: null,

    loading: false,

    error: null,

    setFarms: (farms) =>
      set((state) => {
        /*
         * Keep the currently selected farm
         * if it still exists in the database.
         *
         * Otherwise select the first farm.
         */
        const currentSelection =
          state.selectedFarmId;

        const selectedStillExists =
          currentSelection !== null &&
          farms.some(
            (farm) =>
              farm.id === currentSelection
          );

        return {
          farms,

          selectedFarmId:
            selectedStillExists
              ? currentSelection
              : farms[0]?.id ?? null,

          error: null,
        };
      }),

    loadFarms: async () => {
      /*
       * Avoid starting another request if
       * the store is already loading.
       */
      if (get().loading) {
        return;
      }

      set({
        loading: true,
        error: null,
      });

      try {
        /*
         * This calls:
         *
         * GET /api/farms
         *
         * FastAPI uses the JWT to determine
         * which farmer owns the farms.
         */
        const farms = await getFarms();

        set((state) => {
          const currentSelection =
            state.selectedFarmId;

          const selectedStillExists =
            currentSelection !== null &&
            farms.some(
              (farm) =>
                farm.id === currentSelection
            );

          return {
            farms,

            selectedFarmId:
              selectedStillExists
                ? currentSelection
                : farms[0]?.id ?? null,

            loading: false,

            error: null,
          };
        });
      } catch (error) {
        console.error(
          "Failed to load farms:",
          error
        );

        set({
          loading: false,

          error:
            "Unable to load your farms.",
        });
      }
    },

    addFarm: (farm) =>
      set((state) => {
        /*
         * The farm has already been saved
         * in PostgreSQL by createFarm().
         *
         * We therefore use the ID returned
         * by FastAPI/PostgreSQL.
         */
        const alreadyExists =
          state.farms.some(
            (existingFarm) =>
              existingFarm.id === farm.id
          );

        if (alreadyExists) {
          return {
            farms: state.farms.map(
              (existingFarm) =>
                existingFarm.id === farm.id
                  ? farm
                  : existingFarm
            ),

            selectedFarmId: farm.id,

            error: null,
          };
        }

        return {
          farms: [
            ...state.farms,
            farm,
          ],

          selectedFarmId: farm.id,

          error: null,
        };
      }),

    selectFarm: (farmId) =>
      set((state) => {
        /*
         * Only allow selecting a farm that
         * actually exists in the loaded list.
         */
        const exists =
          state.farms.some(
            (farm) =>
              farm.id === farmId
          );

        if (!exists) {
          return state;
        }

        return {
          selectedFarmId: farmId,
        };
      }),

    removeFarm: (farmId) =>
      set((state) => {
        const farms =
          state.farms.filter(
            (farm) =>
              farm.id !== farmId
          );

        return {
          farms,

          selectedFarmId:
            state.selectedFarmId ===
            farmId
              ? farms[0]?.id ?? null
              : state.selectedFarmId,
        };
      }),

    clearFarms: () =>
      set({
        farms: [],

        selectedFarmId: null,

        error: null,
      }),
  }));