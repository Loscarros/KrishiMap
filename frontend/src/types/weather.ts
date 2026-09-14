export interface WeatherData {
  temperature: number;
  humidity: number;
  rainfall: number;
  precipitationProbability: number;
  windSpeed: number;
  weatherCode: number;
}

export interface DailyWeather {
  date: string;
  temperatureMax: number;
  temperatureMin: number;
  precipitationProbability: number;
  rainfall: number;
  weatherCode: number;
}

export interface WeatherResponse {
  current: WeatherData;
  daily: DailyWeather[];
}