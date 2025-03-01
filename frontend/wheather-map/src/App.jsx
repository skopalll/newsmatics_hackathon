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

  // Handle date change
  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
    // Reset topic and slider when date changes
    setSelectedTopic(null);
    setSliderValue(0);
  };

  // Fetch data from your API when a date is selected (using dummy data here)
  useEffect(() => {
    if (selectedDate) {
      setTimeout(() => {
        const dummyData = {
          "1": { 
            title: "First long title",
            articles: [
              {
                coordinates: { latitude: 40.7128, longitude: -74.0060 },
                title: "Article Title 1",
                summary: "Some details about the article...",
                publishDate: "2025-02-28T09:00:00",
                publisher: "FoxNeeeeeews"
              },
              {
                coordinates: { latitude: 41.8781, longitude: -87.6298 },
                title: "Article Title 2",
                summary: "Additional article details...",
                publishDate: "2025-02-28T11:30:00",
                publisher: "FoxNews"
              },
              {
                coordinates: { latitude: 41.8781, longitude: -87.6298 },
                title: "Article Title 2",
                summary: "Additional article details...",
                publishDate: "2025-02-28T11:30:00",
                publisher: "FoxNews"
              }
            ]
          },
          "2": { 
            title: "Second loooooong title this is the longest title ever written",
            articles: [
              {
                coordinates: { latitude: 34.0522, longitude: -118.2437 },
                title: "Article Title 3",
                summary: "Some details about this article...",
                publishDate: "2025-02-28T08:45:00",
                publisher: "FoxNews"
              }
            ]
          },
          "3": { 
            title: "Third looooooooooooooooong title",
            articles: [
              {
                coordinates: { latitude: 49.384358, longitude: -124.848974 },
                title: "Article Title 2",
                summary: "Additional article details...",
                publishDate: "2025-02-28T11:30:00",
                publisher: "FoxNews"
              },
              {
                coordinates: { latitude: 49.384358, longitude: -66.885444 },
                title: "Article Title 2",
                summary: "Additional article details...",
                publishDate: "2025-02-28T11:30:00",
                publisher: "FoxNews"
              },
              {
                coordinates: { latitude: 24.396308, longitude: -124.848974 },
                title: "Article Title 2",
                summary: "Additional article details...",
                publishDate: "2025-02-28T11:30:00",
                publisher: "FoxNews"
              }
            ]
          }
        };
        setData(dummyData);
        setSelectedTopic("1");
        setSliderValue(0);
      }, 500); // simulate network delay
    }
  }, [selectedDate]);

  // Get full list of articles for the selected topic (all articles)
  const articlesForTopic =
    data && selectedTopic && data[selectedTopic]
      ? data[selectedTopic].articles
      : [];

  // Slider max is based on the count of articles
  const sliderMax = articlesForTopic.length - 1;

  return (
    <div className="App">
      <header>
        <h1>🗣️What happened on:</h1>
        <span className='calendar-emoji'>📅 </span>
        <Calendar value={selectedDate} onChange={handleDateChange} />
      </header>

      {selectedDate && data && (
        <div>
          {/* Topics dropdown */}
          <div className="topics-panel">
            <span className='calendar-emoji'>📰 </span>
            <select onChange={(e) => setSelectedTopic(e.target.value)} value={selectedTopic}>
              <option value="1">{data["1"].title}</option>
              <option value="2">{data["2"].title}</option>
              <option value="3">{data["3"].title}</option>
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
                  Time Stamp: {articlesForTopic[sliderValue].publishDate}
                </div>
              )}
            </div>
          )}

          {/* Pass ALL articles to USMap along with sliderValue */}
          <USMap pins={articlesForTopic} sliderValue={sliderValue} />
        </div>
      )}
    </div>
  );
};

export default App;
