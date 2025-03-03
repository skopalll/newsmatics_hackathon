import 'primereact/resources/themes/bootstrap4-light-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import { Calendar } from 'primereact/calendar';
import React, { useState, useEffect } from 'react';
import USMap from './components/USMap';
import VoteScale from './components/VoteScale.jsx';
import './App.css';

// Format a Date object as "YYYY.MM.DD" using local time.
const formatDateLocal = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}.${month}.${day}`;
};

const App = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [data, setData] = useState(null);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [sliderValue, setSliderValue] = useState(0);
  const [availableDates, setAvailableDates] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/dates')
      .then((response) => response.json())
      .then((avail) => {
        const trimmed = avail.map((d) => d.trim());
        setAvailableDates(trimmed);
      })
      .catch((error) => console.error("Error fetching availability:", error));
  }, []);

  const dateTemplate = (value) => {
    let dateObj;
    let isOtherMonth = false;
  
    if (value && typeof value === 'object' && 'day' in value && 'month' in value && 'year' in value) {
      if ('otherMonth' in value) {
        isOtherMonth = !!value.otherMonth;
      }
      dateObj = new Date(value.year, value.month, value.day);
    } else if (value instanceof Date) {
      dateObj = value;
    } else {
      dateObj = new Date(value);
    }
  
    if (isNaN(dateObj.getTime())) {
      return <span>{JSON.stringify(value)}</span>;
    }
  
    const formatted = formatDateLocal(dateObj);
    const isAvailable = !isOtherMonth && availableDates.includes(formatted);
  
    return (
      <span
        style={{
          color: isAvailable ? 'green' : 'red',
          pointerEvents: isAvailable ? 'auto' : 'none',
          display: 'inline-block',
          width: '100%',
          textAlign: 'center'
        }}
      >
        {dateObj.getDate()}
      </span>
    );
  };
  


  const handleDateChange = (e) => {
    const newDate = e.value;
    const formattedNewDate = formatDateLocal(newDate);
    if (availableDates.includes(formattedNewDate)) {
      setSelectedDate(newDate);
      setSelectedTopic(null);
      setSliderValue(0);
    }
  };

  useEffect(() => {
    if (selectedDate) {
      const formattedDate = formatDateLocal(selectedDate);
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
        .catch((error) => {
          setSelectedTopic(null);
          console.error('Error fetching data:', error);
        });
    }
  }, [selectedDate]);

  const articlesForTopic =
    data && selectedTopic && data[selectedTopic]
      ? data[selectedTopic].articles
      : [];

  const sliderMax = articlesForTopic.length - 1;
  const displayedArticles = articlesForTopic.slice(0, sliderValue + 1);

  return (
    <div className="App">
      <header>
        <h1>🗣️ What happened on:</h1>
        <span className="calendar-emoji">📅 </span>
        <Calendar
          key={availableDates.join(',')} // re-render when availableDates updates
          value={selectedDate}
          onChange={handleDateChange}
          dateTemplate={dateTemplate}
          inline
        />
      </header>

      {selectedTopic && data ? (
        <div>
          {/* Topics dropdown */}
          <div className="topics-panel">
            <span className="calendar-emoji">📰 </span>
            <select
              onChange={(e) => {
                setSelectedTopic(e.target.value);
                setSliderValue(0);
              }}
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

          {/* Vote scale above timeline slider */}
          {selectedTopic && <VoteScale articles={displayedArticles} />}

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

          <USMap pins={articlesForTopic} sliderValue={sliderValue} />
        </div>
      ) : (
        <h2>No data for projection 👎</h2>
      )}
    </div>
  );
};

export default App;