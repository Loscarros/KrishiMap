"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";

export type Language = "en" | "hi" | "bn";

const translations = {
  en: {
    // General
    appName: "KrishiMap",
    tagline: "AI Farm Intelligence",
    farmer: "Farmer",
    farmOwner: "Farm owner",
    currentFarm: "Current farm",
    noFarmSelected: "No farm selected",
    save: "Save",
    cancel: "Cancel",
    create: "Create",
    add: "Add",
    close: "Close",
    loading: "Loading...",

    // Navigation
    workspace: "Workspace",
    dashboard: "Dashboard",
    farmAnalysis: "Farm Analysis",
    farmCalendar: "Farm Calendar",
    myFarms: "My Farms",
    settings: "Settings",
    addFarm: "Add Farm",
    addFirstFarm: "Add your first farm",

    // Header
    notifications: "Notifications",
    unread: "unread",
    markAllRead: "Mark all as read",
    noNotifications: "No new notifications",
    language: "Language",

    // Dashboard
    overview: "Overview",
    welcomeBack: "Welcome back",
    farmOverview: "Farm Overview",
    weather: "Weather",
    todayWeather: "Today's weather",
    humidity: "Humidity",
    rainfall: "Rainfall",
    rainProbability: "Rain probability",
    wind: "Wind",
    cropHealth: "Crop Health",
    good: "Good",
    healthy: "Healthy",
    weatherForecast: "Weather Forecast",
    sevenDayForecast: "7-day weather forecast",
    cropRecommendation: "Crop Recommendation",
    suitability: "Suitability",
    rainfallSuitability: "Rainfall",
    temperatureSuitability: "Temperature",
    soilSuitability: "Soil",
    seasonSuitability: "Season",
    vegetationSuitability: "Vegetation",
    aiAssistant: "AI Assistant",
    askFarmAssistant: "Ask your farm assistant",

    // Analysis
    farmHealthOverview: "Farm Health Overview",
    overall: "Overall",
    overallCondition: "Good Farm Condition",
    overallDescription:
      "Conditions are favorable for the current crop.",
    vegetationIndex: "Vegetation Index",
    weatherSuitability: "Weather Suitability",
    irrigationNeed: "Irrigation Need",
    moderate: "Moderate",
    positive: "Positive",
    farmLocation: "Farm Location",
    spatialOverview: "Spatial overview of your selected farm.",
    aiFarmInsight: "AI Farm Insight",
    automatedInterpretation: "Automated interpretation",
    low: "Low",
    currentCropRecommendation: "Current Crop Recommendation",

    // Calendar
    selectDate: "Select a date to view or add activities.",
    selectedDate: "Selected date",
    upcomingTasks: "Upcoming Tasks",
    nextActivities: "Your next farm activities",
    noTasksScheduled: "No tasks scheduled",
    addActivity: "Add an activity for this date.",
    addFarmTask: "Add Farm Task",
    irrigation: "Irrigation",
    fertilizer: "Fertilizer",
    monitoring: "Monitoring",
    harvest: "Harvest",
    other: "Other",
    taskTypes: "Task types",
    taskAdded: "Added manually from the farm calendar.",
    today: "Today",

    // Farm creation
    addNewFarm: "Add New Farm",
    drawFarmBoundary: "Draw your farm boundary on the map.",
    farmBoundary: "Farm Boundary",
    usePolygon: "Use the polygon tool to outline your field.",
    farmDetails: "Farm Details",
    basicInformation: "Add some basic information about this field.",
    farmName: "Farm name",
    currentCrop: "Current / intended crop",
    selectCrop: "Select crop",
    detectedArea: "Detected area",
    acres: "acres",
    center: "Center",
    saveFarm: "Save Farm",
    farmSaved: "Farm saved successfully.",

    // Notifications
    weatherAlert: "Weather Alert",
    weatherMessage:
      "Rainfall probability is high. Consider delaying irrigation.",
    farmHealthNotification: "Farm Health",
    farmHealthMessage:
      "Your crop health score is currently 82%.",
    fertilizerReminder: "Fertilizer Reminder",
    fertilizerMessage:
      "Fertilizer application is scheduled for tomorrow.",

    // Crops
    rice: "Rice",
    maize: "Maize",
    wheat: "Wheat",
    potato: "Potato",
    tomato: "Tomato",
    otherCrop: "Other",

    // Weather
    clearSky: "Clear sky",
    partlyCloudy: "Partly cloudy",
    foggy: "Foggy",
    drizzle: "Drizzle",
    rain: "Rain",
    snow: "Snow",
    rainShowers: "Rain showers",
    thunderstorm: "Thunderstorm",
  },

  hi: {
    appName: "कृषिमैप",
    tagline: "एआई कृषि बुद्धिमत्ता",
    farmer: "किसान",
    farmOwner: "खेत मालिक",
    currentFarm: "वर्तमान खेत",
    noFarmSelected: "कोई खेत चयनित नहीं",
    save: "सहेजें",
    cancel: "रद्द करें",
    create: "बनाएं",
    add: "जोड़ें",
    close: "बंद करें",
    loading: "लोड हो रहा है...",

    workspace: "कार्यस्थल",
    dashboard: "डैशबोर्ड",
    farmAnalysis: "खेत विश्लेषण",
    farmCalendar: "खेत कैलेंडर",
    myFarms: "मेरे खेत",
    settings: "सेटिंग्स",
    addFarm: "खेत जोड़ें",
    addFirstFarm: "अपना पहला खेत जोड़ें",

    notifications: "सूचनाएं",
    unread: "अपठित",
    markAllRead: "सभी को पढ़ा हुआ करें",
    noNotifications: "कोई नई सूचना नहीं",
    language: "भाषा",

    overview: "अवलोकन",
    welcomeBack: "वापसी पर स्वागत है",
    farmOverview: "खेत का अवलोकन",
    weather: "मौसम",
    todayWeather: "आज का मौसम",
    humidity: "नमी",
    rainfall: "वर्षा",
    rainProbability: "बारिश की संभावना",
    wind: "हवा",
    cropHealth: "फसल स्वास्थ्य",
    good: "अच्छा",
    healthy: "स्वस्थ",
    weatherForecast: "मौसम पूर्वानुमान",
    sevenDayForecast: "7 दिनों का मौसम पूर्वानुमान",
    cropRecommendation: "फसल सुझाव",
    suitability: "उपयुक्तता",
    rainfallSuitability: "वर्षा",
    temperatureSuitability: "तापमान",
    soilSuitability: "मिट्टी",
    seasonSuitability: "मौसम",
    vegetationSuitability: "वनस्पति",
    aiAssistant: "एआई सहायक",
    askFarmAssistant: "अपने कृषि सहायक से पूछें",

    farmHealthOverview: "खेत स्वास्थ्य अवलोकन",
    overall: "कुल",
    overallCondition: "खेत की स्थिति अच्छी है",
    overallDescription:
      "वर्तमान फसल के लिए परिस्थितियां अनुकूल हैं।",
    vegetationIndex: "वनस्पति सूचकांक",
    weatherSuitability: "मौसम उपयुक्तता",
    irrigationNeed: "सिंचाई आवश्यकता",
    moderate: "मध्यम",
    positive: "सकारात्मक",
    farmLocation: "खेत का स्थान",
    spatialOverview: "आपके चयनित खेत का स्थानिक अवलोकन।",
    aiFarmInsight: "एआई कृषि जानकारी",
    automatedInterpretation: "स्वचालित विश्लेषण",
    low: "कम",
    currentCropRecommendation: "वर्तमान फसल सुझाव",

    selectDate: "गतिविधियां देखने या जोड़ने के लिए तारीख चुनें।",
    selectedDate: "चयनित तारीख",
    upcomingTasks: "आगामी कार्य",
    nextActivities: "आपकी अगली कृषि गतिविधियां",
    noTasksScheduled: "कोई कार्य निर्धारित नहीं",
    addActivity: "इस तारीख के लिए गतिविधि जोड़ें।",
    addFarmTask: "कृषि कार्य जोड़ें",
    irrigation: "सिंचाई",
    fertilizer: "उर्वरक",
    monitoring: "निगरानी",
    harvest: "कटाई",
    other: "अन्य",
    taskTypes: "कार्य प्रकार",
    taskAdded: "कृषि कैलेंडर से मैन्युअल रूप से जोड़ा गया।",
    today: "आज",

    addNewFarm: "नया खेत जोड़ें",
    drawFarmBoundary: "मानचित्र पर अपने खेत की सीमा बनाएं।",
    farmBoundary: "खेत की सीमा",
    usePolygon: "अपने खेत की सीमा बनाने के लिए बहुभुज उपकरण का उपयोग करें।",
    farmDetails: "खेत का विवरण",
    basicInformation: "इस खेत के बारे में कुछ मूल जानकारी दें।",
    farmName: "खेत का नाम",
    currentCrop: "वर्तमान / इच्छित फसल",
    selectCrop: "फसल चुनें",
    detectedArea: "पता लगाया गया क्षेत्र",
    acres: "एकड़",
    center: "केंद्र",
    saveFarm: "खेत सहेजें",
    farmSaved: "खेत सफलतापूर्वक सहेजा गया।",

    weatherAlert: "मौसम चेतावनी",
    weatherMessage:
      "बारिश की संभावना अधिक है। सिंचाई कुछ समय के लिए रोकने पर विचार करें।",
    farmHealthNotification: "खेत स्वास्थ्य",
    farmHealthMessage:
      "आपकी फसल का स्वास्थ्य स्कोर वर्तमान में 82% है।",
    fertilizerReminder: "उर्वरक अनुस्मारक",
    fertilizerMessage:
      "उर्वरक डालने का कार्य कल निर्धारित है।",

    rice: "चावल",
    maize: "मक्का",
    wheat: "गेहूं",
    potato: "आलू",
    tomato: "टमाटर",
    otherCrop: "अन्य",

    clearSky: "साफ आसमान",
    partlyCloudy: "आंशिक बादल",
    foggy: "कोहरा",
    drizzle: "बूंदाबांदी",
    rain: "बारिश",
    snow: "बर्फबारी",
    rainShowers: "बारिश की फुहारें",
    thunderstorm: "आंधी-तूफान",
  },

  bn: {
    appName: "কৃষিম্যাপ",
    tagline: "এআই কৃষি বুদ্ধিমত্তা",
    farmer: "কৃষক",
    farmOwner: "খামারের মালিক",
    currentFarm: "বর্তমান খামার",
    noFarmSelected: "কোনও খামার নির্বাচিত নয়",
    save: "সংরক্ষণ",
    cancel: "বাতিল",
    create: "তৈরি করুন",
    add: "যোগ করুন",
    close: "বন্ধ করুন",
    loading: "লোড হচ্ছে...",

    workspace: "ওয়ার্কস্পেস",
    dashboard: "ড্যাশবোর্ড",
    farmAnalysis: "খামার বিশ্লেষণ",
    farmCalendar: "খামার ক্যালেন্ডার",
    myFarms: "আমার খামার",
    settings: "সেটিংস",
    addFarm: "খামার যোগ করুন",
    addFirstFarm: "আপনার প্রথম খামার যোগ করুন",

    notifications: "বিজ্ঞপ্তি",
    unread: "অপঠিত",
    markAllRead: "সব পড়া হয়েছে হিসেবে চিহ্নিত করুন",
    noNotifications: "কোনও নতুন বিজ্ঞপ্তি নেই",
    language: "ভাষা",

    overview: "পর্যালোচনা",
    welcomeBack: "আবার স্বাগতম",
    farmOverview: "খামারের পর্যালোচনা",
    weather: "আবহাওয়া",
    todayWeather: "আজকের আবহাওয়া",
    humidity: "আর্দ্রতা",
    rainfall: "বৃষ্টিপাত",
    rainProbability: "বৃষ্টির সম্ভাবনা",
    wind: "বাতাস",
    cropHealth: "ফসলের স্বাস্থ্য",
    good: "ভালো",
    healthy: "সুস্থ",
    weatherForecast: "আবহাওয়ার পূর্বাভাস",
    sevenDayForecast: "৭ দিনের আবহাওয়ার পূর্বাভাস",
    cropRecommendation: "ফসলের পরামর্শ",
    suitability: "উপযুক্ততা",
    rainfallSuitability: "বৃষ্টিপাত",
    temperatureSuitability: "তাপমাত্রা",
    soilSuitability: "মাটি",
    seasonSuitability: "ঋতু",
    vegetationSuitability: "উদ্ভিদ",
    aiAssistant: "এআই সহকারী",
    askFarmAssistant: "আপনার কৃষি সহকারীকে জিজ্ঞাসা করুন",

    farmHealthOverview: "খামারের স্বাস্থ্য পর্যালোচনা",
    overall: "সামগ্রিক",
    overallCondition: "খামারের অবস্থা ভালো",
    overallDescription:
      "বর্তমান ফসলের জন্য পরিস্থিতি অনুকূল।",
    vegetationIndex: "উদ্ভিদ সূচক",
    weatherSuitability: "আবহাওয়ার উপযুক্ততা",
    irrigationNeed: "সেচের প্রয়োজন",
    moderate: "মাঝারি",
    positive: "ইতিবাচক",
    farmLocation: "খামারের অবস্থান",
    spatialOverview: "আপনার নির্বাচিত খামারের স্থানিক পর্যালোচনা।",
    aiFarmInsight: "এআই খামার তথ্য",
    automatedInterpretation: "স্বয়ংক্রিয় বিশ্লেষণ",
    low: "কম",
    currentCropRecommendation: "বর্তমান ফসলের পরামর্শ",

    selectDate: "কাজ দেখতে বা যোগ করতে একটি তারিখ নির্বাচন করুন।",
    selectedDate: "নির্বাচিত তারিখ",
    upcomingTasks: "আসন্ন কাজ",
    nextActivities: "আপনার পরবর্তী কৃষি কার্যক্রম",
    noTasksScheduled: "কোনও কাজ নির্ধারিত নেই",
    addActivity: "এই তারিখের জন্য একটি কাজ যোগ করুন।",
    addFarmTask: "কৃষি কাজ যোগ করুন",
    irrigation: "সেচ",
    fertilizer: "সার",
    monitoring: "পর্যবেক্ষণ",
    harvest: "ফসল কাটা",
    other: "অন্যান্য",
    taskTypes: "কাজের ধরন",
    taskAdded: "কৃষি ক্যালেন্ডার থেকে ম্যানুয়ালি যোগ করা হয়েছে।",
    today: "আজ",

    addNewFarm: "নতুন খামার যোগ করুন",
    drawFarmBoundary: "মানচিত্রে আপনার খামারের সীমানা আঁকুন।",
    farmBoundary: "খামারের সীমানা",
    usePolygon: "আপনার জমির সীমানা চিহ্নিত করতে বহুভুজ টুল ব্যবহার করুন।",
    farmDetails: "খামারের বিবরণ",
    basicInformation: "এই খামার সম্পর্কে কিছু প্রাথমিক তথ্য যোগ করুন।",
    farmName: "খামারের নাম",
    currentCrop: "বর্তমান / কাঙ্ক্ষিত ফসল",
    selectCrop: "ফসল নির্বাচন করুন",
    detectedArea: "নির্ধারিত এলাকা",
    acres: "একর",
    center: "কেন্দ্র",
    saveFarm: "খামার সংরক্ষণ করুন",
    farmSaved: "খামার সফলভাবে সংরক্ষণ করা হয়েছে।",

    weatherAlert: "আবহাওয়া সতর্কতা",
    weatherMessage:
      "বৃষ্টির সম্ভাবনা বেশি। সেচ কিছু সময়ের জন্য পিছিয়ে দেওয়ার কথা বিবেচনা করুন।",
    farmHealthNotification: "খামারের স্বাস্থ্য",
    farmHealthMessage:
      "আপনার ফসলের স্বাস্থ্য স্কোর বর্তমানে ৮২%।",
    fertilizerReminder: "সার দেওয়ার অনুস্মারক",
    fertilizerMessage:
      "আগামীকাল সার দেওয়ার কাজ নির্ধারিত রয়েছে।",

    rice: "ধান",
    maize: "ভুট্টা",
    wheat: "গম",
    potato: "আলু",
    tomato: "টমেটো",
    otherCrop: "অন্যান্য",

    clearSky: "পরিষ্কার আকাশ",
    partlyCloudy: "আংশিক মেঘলা",
    foggy: "কুয়াশা",
    drizzle: "গুঁড়ি গুঁড়ি বৃষ্টি",
    rain: "বৃষ্টি",
    snow: "তুষারপাত",
    rainShowers: "বৃষ্টির ঝরনা",
    thunderstorm: "বজ্রঝড়",
  },
};

type TranslationKey = keyof typeof translations.en;

interface LanguageContextType {
  language: Language;
  setLanguage: (language: Language) => void;
  t: (key: TranslationKey) => string;
}

const LanguageContext =
  createContext<LanguageContextType | null>(null);

export function LanguageProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [language, setLanguageState] =
    useState<Language>("en");

  useEffect(() => {
    const saved =
      localStorage.getItem("krishimap-language");

    if (
      saved === "en" ||
      saved === "hi" ||
      saved === "bn"
    ) {
      setLanguageState(saved);
    }
  }, []);

  const setLanguage = (newLanguage: Language) => {
    setLanguageState(newLanguage);
    localStorage.setItem(
      "krishimap-language",
      newLanguage
    );
  };

  const t = (key: TranslationKey) => {
    return translations[language][key] ?? translations.en[key];
  };

  return (
    <LanguageContext.Provider
      value={{
        language,
        setLanguage,
        t,
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);

  if (!context) {
    throw new Error(
      "useLanguage must be used inside LanguageProvider"
    );
  }

  return context;
}