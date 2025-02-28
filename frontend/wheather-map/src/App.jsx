// App.jsx
import React, { useState, useEffect } from 'react';
import USMap from './components/USMap';
import './App.css';

const App = () => {
  const [selectedDate, setSelectedDate] = useState('');
  const [data, setData] = useState(null);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [sliderValue, setSliderValue] = useState(0);

  // Handle date change (you can replace this with a calendar library if needed)
  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
    // Reset topic and slider when date changes
    setSelectedTopic(null);
    setSliderValue(0);
  };

  // Fetch data from your API when a date is selected
  useEffect(() => {
    // if (selectedDate) {
    //   fetch(`https://your-api.com/records?date=${selectedDate}`)
    //     .then((response) => response.json())
    //     .then((json) => {
    //       setData(json);
    //       // Optionally, set a default topic (e.g., topic "1")
    //       setSelectedTopic('1');
    //       setSliderValue(0);
    //     })
    //     .catch((error) => console.error('Error fetching data:', error));
    // }
      if (selectedDate) {
        // Simulate API call delay with setTimeout
        setTimeout(() => {
          const dummyData = {
            "1": [
              {
                coordinates: { latitude: 40.7128, longitude: -74.0060 },
                title: "Article Title 1",
                summary: "Some details about the article...",
                publishDate: "2025-02-28T09:00:00"
              },
              {
                coordinates: { latitude: 41.8781, longitude: -87.6298 },
                title: "Article Title 2",
                summary: "Additional article details...",
                publishDate: "2025-02-28T11:30:00"
              }
            ],
            "2": [
              {
                coordinates: { latitude: 34.0522, longitude: -118.2437 },
                title: "Article Title 3",
                summary: "Some details about this article...",
                publishDate: "2025-02-28T08:45:00"
              }
            ],
            "3": [
              {
                coordinates: { latitude: 29.7604, longitude: -95.3698 },
                title: "Article Title 4",
                summary: "More details about this article...",
                publishDate: "2025-02-28T14:30:00"
              }
            ]
          };
          setData(dummyData);
          setSelectedTopic("1");
          setSliderValue(0);
        }, 500); // simulate network delay
      }
  }, [selectedDate]);

  // Determine the articles for the selected topic
  const articlesForTopic =
    data && selectedTopic && data[selectedTopic]
      ? data[selectedTopic]
      : [];

  // The slider will be based on the index of articles in the selected topic
  const sliderMax = articlesForTopic.length - 1;

  // The pins to display: show articles up to the slider's index (cumulative)
  const displayedArticles = articlesForTopic.slice(0, sliderValue + 1);

  return (
    <div className="App">
      <header>
        {/* Date picker */}
        <input type="date" value={selectedDate} onChange={handleDateChange} />
      </header>

      {selectedDate && data && (
        <div>
          {/* Topics panel */}
          <div className="topics-panel">
            <button onClick={() => setSelectedTopic('1')}>Topic 1</button>
            <button onClick={() => setSelectedTopic('2')}>Topic 2</button>
            <button onClick={() => setSelectedTopic('3')}>Topic 3</button>
          </div>

          {/* Timeline slider for the selected topic */}
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
                  Current: {articlesForTopic[sliderValue].publishDate}
                </div>
              )}
            </div>
          )}

          {/* Map with the cumulative pins */}
          <USMap pins={displayedArticles} />
        </div>
      )}
    </div>
  );
};

export default App;
