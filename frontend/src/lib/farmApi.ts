
import { api } from "@/lib/api";

import {
  CreateFarmPayload,
  Farm,
} from "@/types/farm";

interface BackendFarm {
  id: number;
  name: string;
  area_acres: number;
  latitude: number;
  longitude: number;
  boundary: GeoJSON.Polygon;
  crop?: string | null;
}

function normalizeFarm(
  farm: BackendFarm
): Farm {
  return {
    id: String(farm.id),
    name: farm.name,
    areaAcres: farm.area_acres,
    latitude: farm.latitude,
    longitude: farm.longitude,
    boundary: farm.boundary,
    crop: farm.crop ?? undefined,
  };
}

export async function getFarms(): Promise<Farm[]> {
  const response =
    await api.get<BackendFarm[]>(
      "/farms"
    );

  return response.data.map(
    normalizeFarm
  );
}

export async function createFarm(
  payload: CreateFarmPayload
): Promise<Farm> {
  const response =
    await api.post<BackendFarm>(
      "/farms",
      {
        name: payload.name,
        area_acres:
          payload.areaAcres,
        latitude:
          payload.latitude,
        longitude:
          payload.longitude,
        boundary:
          payload.boundary,
        crop:
          payload.crop ?? null,
      }
    );

  return normalizeFarm(
    response.data
  );
}

export async function getFarm(
  farmId: string
): Promise<Farm> {
  const response =
    await api.get<BackendFarm>(
      `/farms/${farmId}`
    );

  return normalizeFarm(
    response.data
  );
}