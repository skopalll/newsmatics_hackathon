import React, { useState } from 'react';
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';

const geoUrl = 'https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json';

const USMap = ({ pins }) => {
  const [hoveredIndex, setHoveredIndex] = useState(null);

  return (
    <ComposableMap projection="geoAlbersUsa" width={800} height={500}>
      <Geographies geography={geoUrl}>
        {({ geographies }) =>
          geographies.map((geo) => (
            // <Geography key={geo.rsmKey} geography={geo} fill="#DDD" stroke="#FFF" />
            <Geography key={geo.rsmKey} geography={geo} fill="#333" stroke="#666" />
          ))
        }
      </Geographies>
      {pins &&
        pins.map((article, index) => (
            <Marker
            key={index}
            coordinates={[ article.coordinates.longitude, article.coordinates.latitude ]}
            onMouseEnter={() => setHoveredIndex(index)}
            onMouseLeave={() => setHoveredIndex(null)}
            >
            {/* Replace the circle with a custom SVG path for a pin */}
            <path
                className="landing-pin"
                d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5S10.62 6.5 12 6.5 14.5 7.62 14.5 9 13.38 11 12 11z"
                fill="#F00"
                // This is the final transform where the tip of the pin should be.
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
                    {article.publisher}
                </text>
                </g>
            )}
            </Marker>

          
        ))}
    </ComposableMap>
  );
};

export default USMap;
