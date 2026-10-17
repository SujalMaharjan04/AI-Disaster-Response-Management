import React from "react";
import { MapContainer, ImageOverlay } from "react-leaflet";
import "leaflet/dist/leaflet.css";

interface MapDisplayProps {
  imageUrl: string;
}

export function MapDisplay({ imageUrl }: MapDisplayProps) {
  // In a real scenario, we'd center the map on the actual GPS coordinates
  // For the demo, we center on a dummy point and overlay the imagery
  const center: [number, number] = [27.7172, 85.324]; // Kathmandu

  return (
    <div className="h-full w-full rounded-xl overflow-hidden border border-slate-700 shadow-2xl">
      <MapContainer
        center={center}
        zoom={13}
        style={{ height: "100%", width: "100%" }}
        zoomControl={false}
      >
        {/* We would add TileLayers here, but for the demo we focus on the imagery overlay */}
        <ImageOverlay
          url={imageUrl}
          bounds={[
            [27.7, 85.3],
            [27.8, 85.4],
          ]}
        />
      </MapContainer>
    </div>
  );
}
