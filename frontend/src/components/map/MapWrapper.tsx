"use client";

import dynamic from "next/dynamic";

const FarmMap = dynamic(
  () => import("./FarmMap"),
  {
    ssr: false,

    loading: () => (
      <div className="flex h-full min-h-[500px] items-center justify-center rounded-2xl bg-slate-100">
        <p className="text-sm text-slate-500">
          Loading map...
        </p>
      </div>
    ),
  }
);

interface MapWrapperProps {
  center?: [number, number];

  userLocation?: [number, number];

  boundary?: GeoJSON.Polygon;

  onFarmDrawn?: (
    polygon: GeoJSON.Polygon,
    areaAcres: number,
    center: [number, number]
  ) => void;
}

export default function MapWrapper({
  center,
  userLocation,
  boundary,
  onFarmDrawn,
}: MapWrapperProps) {
  return (
    <FarmMap
      center={center}
      userLocation={userLocation}
      boundary={boundary}
      onFarmDrawn={onFarmDrawn}
    />
  );
}