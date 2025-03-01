// App.jsx
import 'primereact/resources/themes/bootstrap4-light-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import { Calendar } from 'primereact/calendar';
import React, { useState, useEffect } from 'react';
import USMap from './components/USMap';
import './App.css';
import VoteScale from './components/VoteScale.jsx';

// Format date using local time (YYYY.MM.DD)
const formatDateLocal = (date) => {
  const year = date.getFullYear();
  const month = ('0' + (date.getMonth() + 1)).slice(-2);
  const day = ('0' + date.getDate()).slice(-2);
  return `${year}.${month}.${day}`;
};

const App = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [data, setData] = useState(null);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [sliderValue, setSliderValue] = useState(0);

  // When the date changes, update the selected date and reset topic/slider
  const handleDateChange = (e) => {
    // The Calendar returns a Date object in e.value
    setSelectedDate(e.value);
    setSelectedTopic(null);
    setSliderValue(0);
  };

  // Fetch data from the API whenever the selected date changes.
  useEffect(() => {
    if (selectedDate) {
      // Format date as "YYYY.MM.DD" using local time
      const formattedDate = formatDateLocal(selectedDate);
      console.log(`http://localhost:5001/date?date=${formattedDate}`);
      // If running in Docker, you might use "http://backend:5000" instead of localhost.
      fetch(`http://localhost:5001/date?date=${formattedDate}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((json) => {
          setData(json);
          // Automatically select the first topic (keys "0", "1", etc.)
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
  // Each article is an array of 8 elements.
  const articlesForTopic =
    data && selectedTopic && data[selectedTopic]
      ? data[selectedTopic].articles
      : [];

  // The slider max is determined by the number of articles.
  const sliderMax = articlesForTopic.length - 1;

  // We'll display cumulative articles on the map based on the slider value.
  const displayedArticles = articlesForTopic.slice(0, sliderValue + 1);

  return (
    <div className="App">
      <header>
        <h1>🗣️ What happened on:</h1>
        <span className='calendar-emoji'>📅 </span>
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

          {/* Vote scale above the timeline slider */}
          {selectedTopic && (
            <VoteScale articles={displayedArticles} />
          )}

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

          {/* Pass all articles to USMap so it can render coordinates based on the slider */}
          <USMap pins={articlesForTopic} sliderValue={sliderValue} />
        </div>
      ) : <h2>No data for projection 👎</h2>}
    </div>
  );
};

export default App;
