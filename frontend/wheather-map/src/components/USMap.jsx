import React, { useState, useRef, useEffect } from 'react';
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';

const geoUrl = 'https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json';

// Jitter function to add a small random offset to coordinates
const jitterCoordinates = (coords, factor = 0.02) => {
  return [
    coords[0] + (Math.random() - 0.5) * factor,
    coords[1] + (Math.random() - 0.5) * factor,
  ];
};

const USMap = ({ pins }) => {
  const [hoveredIndex, setHoveredIndex] = useState(null);
  // useRef to store a mapping of pin index to jittered coordinates.
  const jitterMapping = useRef({});

  // Whenever the pins prop changes, update the jitterMapping
  useEffect(() => {
    pins.forEach((pin, index) => {
      // Only calculate jitter if it hasn't been done for this index already.
      if (!jitterMapping.current.hasOwnProperty(index)) {
        jitterMapping.current[index] = jitterCoordinates(
          [pin.coordinates.longitude, pin.coordinates.latitude],
          1
        );
      }
    });
  }, [pins]);

  return (
    <ComposableMap projection="geoAlbersUsa" width={800} height={500}>
      <Geographies geography={geoUrl}>
        {({ geographies }) =>
          geographies.map((geo) => (
            <Geography key={geo.rsmKey} geography={geo} fill="#333" stroke="#666" />
          ))
        }
      </Geographies>
      {pins.map((pin, index) => (
        <Marker
          key={index}
          // Use jittered coordinates if available, otherwise fallback to the raw coordinates
          coordinates={jitterMapping.current[index] || [pin.coordinates.longitude, pin.coordinates.latitude]}
          onMouseEnter={() => setHoveredIndex(index)}
          onMouseLeave={() => setHoveredIndex(null)}
        >
          <path
            className="landing-pin"
            d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5S10.62 6.5 12 6.5 14.5 7.62 14.5 9 13.38 11 12 11z"
            fill="#F00"
            transform="translate(-12, -24) scale(1.5)"
          />
          {hoveredIndex === index && (
            <g transform="translate(0, -20)">
              <rect 
                x="-45" 
                y="-10" 
                width="90" 
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
                {pin.publisher}
              </text>
            </g>
          )}
        </Marker>
      ))}
    </ComposableMap>
  );
};

export default USMap;
