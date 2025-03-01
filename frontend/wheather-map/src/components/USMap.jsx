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

const USMap = ({ pins, sliderValue }) => {
  const [hoveredIndex, setHoveredIndex] = useState(null);
  const [jitteredPins, setJitteredPins] = useState([]);

  useEffect(() => {
    if (pins && pins.length > 0) {
      const updated = pins.map((article) => {
        // article[3] for latitude and article[4] for longitude.
        const rawCoords = [article[4], article[3]];
        return {
          article,
          jitteredCoordinates: jitterCoordinates(rawCoords, 1),
        };
      });
      setJitteredPins(updated);
    }
  }, [pins]);

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
        const pinColor = orientationColors[article[5]] || "#F00";
        
        // Tooltip: use article[0] as the text (convert to string if needed)
        const tooltipText = String(article[0]);
        const padding = 20; // total padding (left+right)
        const approxCharWidth = 7; // approximate width per character in pixels at fontSize=12
        // Calculate the dynamic width, with a minimum width of 90 pixels
        const rectWidth = Math.max(90, tooltipText.length * approxCharWidth + padding);
        const rectX = -rectWidth / 2; // center the rectangle horizontally

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
