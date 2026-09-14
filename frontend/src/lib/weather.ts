
import { Language } from "@/context/LanguageContext";

export function getWeatherDescription(
  code: number | null | undefined,
  language: Language = "en"
) {
  if (
    code === null ||
    code === undefined
  ) {
    return getUnknownWeather(language);
  }

  if (code === 0) {
    return getWeatherTranslation(
      "clearSky",
      language
    );
  }

  if ([1, 2, 3].includes(code)) {
    return getWeatherTranslation(
      "partlyCloudy",
      language
    );
  }

  if ([45, 48].includes(code)) {
    return getWeatherTranslation(
      "foggy",
      language
    );
  }

  if ([51, 53, 55].includes(code)) {
    return getWeatherTranslation(
      "drizzle",
      language
    );
  }

  if ([61, 63, 65].includes(code)) {
    return getWeatherTranslation(
      "rain",
      language
    );
  }

  if ([71, 73, 75].includes(code)) {
    return getWeatherTranslation(
      "snow",
      language
    );
  }

  if ([80, 81, 82].includes(code)) {
    return getWeatherTranslation(
      "rainShowers",
      language
    );
  }

  if ([95, 96, 99].includes(code)) {
    return getWeatherTranslation(
      "thunderstorm",
      language
    );
  }

  return getUnknownWeather(language);
}

function getWeatherTranslation(
  key:
    | "clearSky"
    | "partlyCloudy"
    | "foggy"
    | "drizzle"
    | "rain"
    | "snow"
    | "rainShowers"
    | "thunderstorm",
  language: Language
) {
  const translations = {
    clearSky: {
      en: "Clear sky",
      hi: "साफ आसमान",
      bn: "পরিষ্কার আকাশ",
    },

    partlyCloudy: {
      en: "Partly cloudy",
      hi: "आंशिक रूप से बादल",
      bn: "আংশিক মেঘলা",
    },

    foggy: {
      en: "Foggy",
      hi: "कोहरा",
      bn: "কুয়াশাচ্ছন্ন",
    },

    drizzle: {
      en: "Drizzle",
      hi: "बूंदाबांदी",
      bn: "গুঁড়ি গুঁড়ি বৃষ্টি",
    },

    rain: {
      en: "Rain",
      hi: "बारिश",
      bn: "বৃষ্টি",
    },

    snow: {
      en: "Snow",
      hi: "बर्फबारी",
      bn: "তুষারপাত",
    },

    rainShowers: {
      en: "Rain showers",
      hi: "बारिश की फुहार",
      bn: "বৃষ্টির ঝরনা",
    },

    thunderstorm: {
      en: "Thunderstorm",
      hi: "गरज के साथ बारिश",
      bn: "বজ্রঝড়",
    },
  };

  return translations[key][language];
}

function getUnknownWeather(
  language: Language
) {
  switch (language) {
    case "hi":
      return "अज्ञात मौसम";

    case "bn":
      return "অজানা আবহাওয়া";

    case "en":
    default:
      return "Unknown";
  }
}

export function getWeatherIcon(
  code: number | null | undefined
) {
  if (
    code === null ||
    code === undefined
  ) {
    return "🌤️";
  }

  if (code === 0) {
    return "☀️";
  }

  if ([1, 2, 3].includes(code)) {
    return "⛅";
  }

  if ([45, 48].includes(code)) {
    return "🌫️";
  }

  if ([51, 53, 55].includes(code)) {
    return "🌦️";
  }

  if ([61, 63, 65].includes(code)) {
    return "🌧️";
  }

  if ([71, 73, 75].includes(code)) {
    return "❄️";
  }

  if ([80, 81, 82].includes(code)) {
    return "🌦️";
  }

  if ([95, 96, 99].includes(code)) {
    return "⛈️";
  }

  return "🌤️";
}