// App.jsx
import 'primereact/resources/themes/bootstrap4-light-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import { Calendar } from 'primereact/calendar';
import React, { useState, useEffect } from 'react';
import USMap from './components/USMap';
import './App.css';

const App = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [data, setData] = useState(null);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [sliderValue, setSliderValue] = useState(0);

  // When the date changes, update the selected date and reset topic/slider
  const handleDateChange = (e) => {
    // The Calendar returns a Date object
    setSelectedDate(e.value);
    setSelectedTopic(null);
    setSliderValue(0);
  };

  const formatDateLocal = (date) => {
    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2);
    const day = ('0' + date.getDate()).slice(-2);
    return `${year}.${month}.${day}`;
  };

  // Fetch data from the API whenever the selected date changes.
  useEffect(() => {
    if (selectedDate) {
      // Use the local formatting function
      const formattedDate = formatDateLocal(selectedDate);
      console.log(`http://localhost:5001/date?date=${formattedDate}`);
      fetch(`http://localhost:5001/date?date=${formattedDate}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((json) => {
          setData(json);
          const keys = Object.keys(json);
          if (keys.length > 0) {
            setSelectedTopic(keys[0]);
          }
          setSliderValue(0);
        })
        .catch((error) => console.error('Error fetching data:', error));
    }
  }, [selectedDate]);

  // Determine the articles for the selected topic.
  // Each article is expected to be an array with:
  // [0] article id, [1] article title, [2] publish date/time,
  // [3] latitude, [4] longitude, [5] political orientation,
  // [6] credibility, [7] link to the article.
  const articlesForTopic =
    data && selectedTopic && data[selectedTopic]
      ? data[selectedTopic].articles
      : [];

  // The slider max is determined by the number of articles.
  const sliderMax = articlesForTopic.length - 1;

  return (
    <div className="App">
      <header>
        <h1>🗣️ What happened on:</h1>
        <span className="calendar-emoji">📅 </span>
        <Calendar value={selectedDate} onChange={handleDateChange} />
      </header>

      {selectedDate && data ? (
        <div>
          {/* Topics dropdown */}
          <div className="topics-panel">
            <span className="calendar-emoji">📰 </span>
            <select
              onChange={(e) => {
                setSelectedTopic(e.target.value)
                setSliderValue(0)}}
              value={selectedTopic || ''}
            >
              {data &&
                Object.keys(data).map((key) => (
                  <option key={key} value={key}>
                    {data[key].title}
                  </option>
                ))}
            </select>
          </div>

          {/* Timeline slider */}
          {selectedTopic && (
            <div className="slider-panel">
              <input
                type="range"
                min="0"
                max={sliderMax > 0 ? sliderMax : 0}
                value={sliderValue}
                onChange={(e) => setSliderValue(Number(e.target.value))}
              />
              {articlesForTopic[sliderValue] && (
                <div className="timestamp">
                  Time Stamp: {articlesForTopic[sliderValue][2]}
                </div>
              )}
            </div>
          )}

          {/* Pass all articles to USMap so it can render all coordinates and then display a cumulative subset */}
          <USMap pins={articlesForTopic} sliderValue={sliderValue} />
        </div>
      ) : <h2>No data to project 👎</h2>}
    </div>
  );
};

export default App;
