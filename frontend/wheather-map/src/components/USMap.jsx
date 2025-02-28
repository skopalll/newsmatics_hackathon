// // components/USMap.jsx
// import React from 'react';
// import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';

// const geoUrl = 'https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json';

// const USMap = ({ pins }) => {
//   return (
//     <ComposableMap projection="geoAlbersUsa" width={800} height={500}>
//       <Geographies geography={geoUrl}>
//         {({ geographies }) =>
//           geographies.map((geo) => (
//             <Geography key={geo.rsmKey} geography={geo} fill="#DDD" stroke="#FFF" />
//           ))
//         }
//       </Geographies>
//       {pins &&
//         pins.map((article, index) => (
//           <Marker
//             key={index}
//             coordinates={[
//               article.coordinates.longitude,
//               article.coordinates.latitude,
//             ]}
//           >
//             <circle r={5} fill="#F00" stroke="#fff" strokeWidth={2} />
//           </Marker>
//         ))}
//     </ComposableMap>
//   );
// };

// export default USMap;

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
            <Geography key={geo.rsmKey} geography={geo} fill="#DDD" stroke="#FFF" />
          ))
        }
      </Geographies>
      {pins &&
        pins.map((article, index) => (
          <Marker
            key={index}
            coordinates={[
              article.coordinates.longitude,
              article.coordinates.latitude,
            ]}
            onMouseEnter={() => setHoveredIndex(index)}
            onMouseLeave={() => setHoveredIndex(null)}
          >
            <circle r={5} fill="#F00" stroke="#fff" strokeWidth={2} />
            {hoveredIndex === index && (
              <text
                x={0}
                y={-10}
                textAnchor="middle"
                style={{
                  fontSize: '12px',
                  fill: '#000',
                  // Optionally add background styling using a foreignObject or additional CSS
                }}
              >
                {article.publisher}
              </text>
            )}
          </Marker>
        ))}
    </ComposableMap>
  );
};

export default USMap;
