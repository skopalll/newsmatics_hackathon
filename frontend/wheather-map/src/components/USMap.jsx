// USMap.jsx
import React, { useState, useEffect } from 'react';
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';

const geoUrl = 'https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json';

// Jitter function: adds a small random offset to coordinates
const jitterCoordinates = (coords, factor = 0.02) => {
  return [
    coords[0] + (Math.random() - 0.5) * factor,
    coords[1] + (Math.random() - 0.5) * factor,
  ];
};

const orientationColors = {
  "Right-wing": "#BC291E",
  "Center-right": "#ED9993",
  "Neutral": "#f9EEDB",
  "Center-left": "#A7D9FF",
  "Left-wing": "#0070C0",
  "Public Broadcaster": "#FFD966",
  "Gov't Institution": "#E8891D",
  "Pro-Government": "#A35D11",
  "Gov't Propaganda": "#000000",
  "Indeterminate": "#D9D9D9",
  "Pending": "#A1A1AA"
};

// Check that coords is an array of 2 valid numbers
const isValidCoordinate = (coords) =>
  Array.isArray(coords) &&
  coords.length === 2 &&
  typeof coords[0] === 'number' &&
  typeof coords[1] === 'number' &&
  !isNaN(coords[0]) &&
  !isNaN(coords[1]);

// Define a bounding box for the continental U.S.
// (These are approximate values: lat between ~24.4 and 49.4, lon between ~-124.8 and -66.9)
const isWithinUSBounds = (lat, lon) => {
  return lat >= 24.396308 && lat <= 49.384358 && lon >= -124.848974 && lon <= -66.885444;
};

const USMap = ({ pins, sliderValue }) => {
  const [hoveredIndex, setHoveredIndex] = useState(null);
  const [jitteredPins, setJitteredPins] = useState([]);

  useEffect(() => {
    if (pins && pins.length > 0) {
      const updated = pins
        .map((article) => {
          // article[3]: latitude, article[4]: longitude
          const lat = article[3];
          const lon = article[4];
          // Skip if out of bounds
          if (!isWithinUSBounds(lat, lon)) {
            return null;
          }
          const rawCoords = [lon, lat]; // expected order: [longitude, latitude]
          return {
            article,
            jitteredCoordinates: jitterCoordinates(rawCoords, 1),
          };
        })
        .filter((item) => item !== null);
      setJitteredPins(updated);
    }
  }, [pins]);

  // Determine the cumulative subset of pins to display based on sliderValue.
  const displayedPins = jitteredPins.slice(0, sliderValue + 1);

  return (
    <ComposableMap projection="geoAlbersUsa" width={800} height={500}>
      <Geographies geography={geoUrl}>
        {({ geographies }) =>
          geographies.map((geo) => (
            <Geography key={geo.rsmKey} geography={geo} fill="#333" stroke="#666" />
          ))
        }
      </Geographies>
      {displayedPins.map((item, index) => {
        const { article, jitteredCoordinates } = item;
        // Ensure valid jittered coordinates
        if (!isValidCoordinate(jitteredCoordinates)) return null;
        const pinColor = orientationColors[article[5]] || "#F00";
        const tooltipText = String(article[0]); // using article title for tooltip
        const padding = 20; // total horizontal padding
        const approxCharWidth = 9; // approximate pixel width per character (for fontSize 12)
        const rectWidth = tooltipText.length * approxCharWidth + padding;
        const rectX = -rectWidth / 2; // center the rectangle
        return (
          <Marker
            key={index}
            coordinates={jitteredCoordinates}
            onMouseEnter={() => setHoveredIndex(index)}
            onMouseLeave={() => setHoveredIndex(null)}
          >
            <a href={article[7]} target="_blank" rel="noopener noreferrer">
              <path
                className="landing-pin"
                fill={pinColor}
                d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5S10.62 6.5 12 6.5 14.5 7.62 14.5 9 13.38 11 12 11z"
                transform="translate(-12, -24) scale(1.5)"
              />
            </a>
            {hoveredIndex === index && (
              <g transform="translate(0, -20)">
                <rect
                  x={rectX}
                  y="-10"
                  width={rectWidth}
                  height="20"
                  fill="#333"
                  rx="4"
                  ry="4"
                />
                <text
                  x="0"
                  y="0"
                  textAnchor="middle"
                  alignmentBaseline="middle"
                  fontSize="12"
                  fill="#fff"
                >
                  {tooltipText}
                </text>
              </g>
            )}
          </Marker>
        );
      })}
    </ComposableMap>
  );
};

export default USMap;
