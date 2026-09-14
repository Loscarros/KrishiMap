
import { api } from "@/lib/api";
import { WeatherResponse } from "@/types/weather";

export async function getFarmWeather(
  farmId: string
): Promise<WeatherResponse> {
  const response =
    await api.get<WeatherResponse>(
      `/weather/farm/${farmId}`
    );

  return response.data;
}

export async function getMyWeather(): Promise<WeatherResponse> {
  const response =
    await api.get<WeatherResponse>(
      "/weather/me"
    );

  return response.data;
}