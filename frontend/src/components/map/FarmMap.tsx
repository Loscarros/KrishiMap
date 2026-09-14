"use client";

import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  GeoJSON,
  MapContainer,
  TileLayer,
  useMap,
} from "react-leaflet";

import L from "leaflet";

import "@geoman-io/leaflet-geoman-free";
import "@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css";
import "leaflet/dist/leaflet.css";

import { area as turfArea } from "@turf/area";

import {
  Language,
  useLanguage,
} from "@/context/LanguageContext";

interface FarmMapProps {
  center?: [number, number];

  userLocation?: [number, number];

  boundary?: GeoJSON.Polygon;

  onFarmDrawn?: (
    polygon: GeoJSON.Polygon,
    areaAcres: number,
    center: [number, number]
  ) => void;
}

const DEFAULT_CENTER: [number, number] = [
  20.2961,
  85.8245,
];

const DEFAULT_ZOOM = 13;

function MapCenter({
  center,
}: {
  center?: [number, number];
}) {
  const map = useMap();

  const previousCenter = useRef<
    [number, number] | null
  >(null);

  useEffect(() => {
    if (!center) {
      return;
    }

    if (
      previousCenter.current &&
      previousCenter.current[0] === center[0] &&
      previousCenter.current[1] === center[1]
    ) {
      return;
    }

    previousCenter.current = center;

    map.flyTo(center, 15, {
      animate: true,
      duration: 1.5,
    });
  }, [center, map]);

  return null;
}

function UserLocationMarker({
  center,
}: {
  center?: [number, number];
}) {
  const map = useMap();
  const { language } = useLanguage();

  useEffect(() => {
    if (!center) {
      return;
    }

    const marker = L.circleMarker(center, {
      radius: 8,
      color: "#ffffff",
      weight: 3,
      fillColor: "#059669",
      fillOpacity: 1,
    }).addTo(map);

    marker.bindPopup(
      getCurrentLocationLabel(language)
    );

    return () => {
      marker.remove();
    };
  }, [center, map, language]);

  return null;
}

function FarmDrawingControls({
  onFarmDrawn,
}: {
  onFarmDrawn?: FarmMapProps["onFarmDrawn"];
}) {
  const map = useMap();
  const { language } = useLanguage();

  const callbackRef = useRef(onFarmDrawn);

  const [drawing, setDrawing] =
    useState(false);

  const [geomanReady, setGeomanReady] =
    useState(false);

  useEffect(() => {
    callbackRef.current = onFarmDrawn;
  }, [onFarmDrawn]);

  useEffect(() => {
    const pm = (map as any).pm;

    if (!pm) {
      console.error(
        getMapErrorMessage(language)
      );

      return;
    }

    setGeomanReady(true);

    const handleCreate = (event: any) => {
      const layer = event?.layer;

      if (!layer) {
        return;
      }

      if (
        !(
          layer instanceof L.Polygon ||
          layer instanceof L.Rectangle
        )
      ) {
        return;
      }

      if (
        typeof layer.getLatLngs !==
        "function"
      ) {
        return;
      }

      const rawLatLngs =
        layer.getLatLngs();

      if (!Array.isArray(rawLatLngs)) {
        return;
      }

      /*
       * Leaflet's getLatLngs() has a broad
       * TypeScript return type:
       *
       * LatLng[] | LatLng[][]
       *
       * For the Polygon/Rectangle created
       * by Geoman, the first item is the
       * first polygon ring.
       *
       * Explicitly narrow it to LatLng[]
       * so point.lat and point.lng are valid.
       */
      const firstRing =
        rawLatLngs[0] as L.LatLng[];

      if (!Array.isArray(firstRing)) {
        return;
      }

      const coordinates: [
        number,
        number
      ][] = [];

      for (const point of firstRing) {
        if (
          point &&
          typeof point.lat === "number" &&
          typeof point.lng === "number"
        ) {
          coordinates.push([
            point.lng,
            point.lat,
          ]);
        }
      }

      if (coordinates.length < 3) {
        return;
      }

      const first =
        coordinates[0];

      const last =
        coordinates[
          coordinates.length - 1
        ];

      if (
        first[0] !== last[0] ||
        first[1] !== last[1]
      ) {
        coordinates.push([
          first[0],
          first[1],
        ]);
      }

      const polygon: GeoJSON.Polygon = {
        type: "Polygon",
        coordinates: [coordinates],
      };

      const areaSquareMeters =
        turfArea({
          type: "Feature",
          properties: {},
          geometry: polygon,
        });

      const areaAcres =
        areaSquareMeters * 0.000247105;

      if (
        !Number.isFinite(areaAcres) ||
        areaAcres <= 0
      ) {
        return;
      }

      if (
        typeof layer.getBounds !==
        "function"
      ) {
        return;
      }

      const bounds =
        layer.getBounds();

      if (
        !bounds ||
        !bounds.isValid()
      ) {
        return;
      }

      const farmCenter =
        bounds.getCenter();

      callbackRef.current?.(
        polygon,
        Number(
          areaAcres.toFixed(3)
        ),
        [
          farmCenter.lat,
          farmCenter.lng,
        ]
      );

      setDrawing(false);

      try {
        pm.disableDraw();
      } catch {
        // Ignore cleanup errors.
      }
    };

    map.on(
      "pm:create",
      handleCreate
    );

    return () => {
      map.off(
        "pm:create",
        handleCreate
      );
    };
  }, [map, language]);

  const startDrawing = () => {
    const pm = (map as any).pm;

    if (!pm) {
      return;
    }

    try {
      if (drawing) {
        pm.disableDraw();
        setDrawing(false);
        return;
      }

      pm.enableDraw(
        "Polygon",
        {
          allowSelfIntersection: false,

          templineStyle: {
            color: "#059669",
            weight: 2,
          },

          hintlineStyle: {
            color: "#059669",
            dashArray: [5, 5],
          },

          pathOptions: {
            color: "#059669",
            weight: 3,
            fillColor: "#10b981",
            fillOpacity: 0.25,
          },
        }
      );

      setDrawing(true);
    } catch (error) {
      console.error(
        "Failed to start farm drawing:",
        error
      );

      setDrawing(false);
    }
  };

  if (!geomanReady) {
    return null;
  }

  return (
    <div className="absolute left-4 top-4 z-[500]">
      <button
        type="button"
        onClick={startDrawing}
        className={`rounded-xl border px-4 py-2.5 text-sm font-medium shadow-lg backdrop-blur transition ${
          drawing
            ? "border-red-200 bg-red-50 text-red-700 hover:bg-red-100"
            : "border-slate-200 bg-white/95 text-slate-700 hover:border-emerald-300 hover:bg-emerald-50 hover:text-emerald-700"
        }`}
      >
        {drawing
          ? getCancelDrawingLabel(language)
          : getDrawFarmLabel(language)}
      </button>
    </div>
  );
}

function getDrawFarmLabel(
  language: Language
) {
  switch (language) {
    case "hi":
      return "खेत की सीमा बनाएं";

    case "bn":
      return "জমির সীমানা আঁকুন";

    case "en":
    default:
      return "Draw Farm Boundary";
  }
}

function getCancelDrawingLabel(
  language: Language
) {
  switch (language) {
    case "hi":
      return "आरेखण रद्द करें";

    case "bn":
      return "আঁকা বাতিল করুন";

    case "en":
    default:
      return "Cancel Drawing";
  }
}

function getMapErrorMessage(
  language: Language
) {
  switch (language) {
    case "hi":
      return "लीफलेट-जियोमैन मानचित्र उपकरण प्रारंभ नहीं हो सका।";

    case "bn":
      return "লিফলেট-জিওম্যান ম্যাপ টুল চালু করা যায়নি।";

    case "en":
    default:
      return "Leaflet-Geoman failed to initialize.";
  }
}

function getMapHint(
  language: Language
) {
  switch (language) {
    case "hi":
      return "मानचित्र पर खेत की सीमा बनाएं";

    case "bn":
      return "মানচিত্রে জমির সীমানা আঁকুন";

    case "en":
    default:
      return "Draw your farm boundary on the map";
  }
}

function getCurrentLocationLabel(
  language: Language
) {
  switch (language) {
    case "hi":
      return "आपका वर्तमान स्थान";

    case "bn":
      return "আপনার বর্তমান অবস্থান";

    case "en":
    default:
      return "Your current location";
  }
}

export default function FarmMap({
  center,
  userLocation,
  boundary,
  onFarmDrawn,
}: FarmMapProps) {
  const { language } = useLanguage();

  return (
    <div className="relative h-full min-h-[500px] w-full overflow-hidden rounded-2xl">
      <MapContainer
        center={
          center ??
          userLocation ??
          DEFAULT_CENTER
        }
        zoom={DEFAULT_ZOOM}
        scrollWheelZoom={true}
        className="relative z-0 h-full min-h-[500px] w-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {boundary && (
          <GeoJSON
            data={boundary}
            style={{
              color: "#059669",
              weight: 3,
              fillColor: "#10b981",
              fillOpacity: 0.25,
            }}
          />
        )}

        <MapCenter
          center={
            center ??
            userLocation
          }
        />

        <UserLocationMarker
          center={userLocation}
        />

        <FarmDrawingControls
          onFarmDrawn={onFarmDrawn}
        />
      </MapContainer>

      <div className="pointer-events-none absolute bottom-4 left-4 z-[400] rounded-xl border border-slate-200 bg-white/95 px-3 py-2 text-xs text-slate-600 shadow-sm backdrop-blur">
        {getMapHint(language)}
      </div>
    </div>
  );
}