export interface Farm {
  id: string;
  name: string;
  areaAcres: number;
  latitude: number;
  longitude: number;
  boundary?: GeoJSON.Polygon;
  crop?: string;
}

export interface CreateFarmPayload {
  name: string;
  areaAcres: number;
  latitude: number;
  longitude: number;
  boundary: GeoJSON.Polygon;
  crop?: string;
}

export interface FarmSummary {
  id: string;
  name: string;
  areaAcres: number;
  crop?: string;
}