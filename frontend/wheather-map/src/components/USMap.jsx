import React, { useEffect, useState } from 'react';
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';

// URL for US map topology (TopoJSON)
const geoUrl = 'https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json';

const USMap = () => {
//   const [pins, setPins] = useState([]);

  // Fetch coordinates from your API
//   useEffect(() => {
//     fetch('https://your-api.com/coordinates')
//       .then(response => response.json())
//       .then(data => setPins(data))
//       .catch(error => console.error('Error fetching coordinates:', error));
//   }, []);

  return (
    <ComposableMap projection="geoAlbersUsa" width={800} height={500}>
      <Geographies geography={geoUrl}>
        {({ geographies }) =>
          geographies.map(geo => (
            <Geography key={geo.rsmKey} geography={geo} fill="#DDD" stroke="#FFF" />
          ))
        }
      </Geographies>
      {/* {pins.map((pin, index) => (
        <Marker key={index} coordinates={[pin.longitude, pin.latitude]}>
          <circle r={5} fill="#F00" stroke="#fff" strokeWidth={2} />
        </Marker>
      ))} */}
    </ComposableMap>
  );
};

export default USMap;
