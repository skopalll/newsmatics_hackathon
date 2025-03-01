import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "log.txt")
DB_FILE = os.path.join(os.path.dirname(__file__), "..", "database", "sqlite.db")
MAP_FILE = os.path.join(os.path.dirname(__file__), "..", "database", "cities.db")
API_BASE_URL = "https://www.newsmatics.com/news-index"
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NDA0MDAxMTgsInN1YiI6NDMyLCJleHAiOjIwNTU3NjAxMTguMCwic2NvcGVzIjpbImFsbCJdfQ.ZgWINtJswrrJGeVH0GrDG7LZGgv57Y5anU6YBag9edo" 
CAPITALS = {
    "Alabama": "Montgomery",
    "Alaska": "Juneau",
    "Arizona": "Phoenix",
    "Arkansas": "Little Rock",
    "California": "Sacramento",
    "Colorado": "Denver",
    "Connecticut": "Hartford",
    "Delaware": "Dover",
    "Florida": "Tallahassee",
    "Georgia": "Atlanta",
    "Hawaii": "Honolulu",
    "Idaho": "Boise",
    "Illinois": "Springfield",
    "Indiana": "Indianapolis",
    "Iowa": "Des Moines",
    "Kansas": "Topeka",
    "Kentucky": "Frankfort",
    "Louisiana": "Baton Rouge",
    "Maine": "Augusta",
    "Maryland": "Annapolis",
    "Massachusetts": "Boston",
    "Michigan": "Lansing",
    "Minnesota": "Saint Paul",
    "Mississippi": "Jackson",
    "Missouri": "Jefferson City",
    "Montana": "Helena",
    "Nebraska": "Lincoln",
    "Nevada": "Carson City",
    "New Hampshire": "Concord",
    "New Jersey": "Trenton",
    "New Mexico": "Santa Fe",
    "New York": "Albany",
    "North Carolina": "Raleigh",
    "North Dakota": "Bismarck",
    "Ohio": "Columbus",
    "Oklahoma": "Oklahoma City",
    "Oregon": "Salem",
    "Pennsylvania": "Harrisburg",
    "Rhode Island": "Providence",
    "South Carolina": "Columbia",
    "South Dakota": "Pierre",
    "Tennessee": "Nashville",
    "Texas": "Austin",
    "Utah": "Salt Lake City",
    "Vermont": "Montpelier",
    "Virginia": "Richmond",
    "Washington": "Olympia",
    "West Virginia": "Charleston",
    "Wisconsin": "Madison",
    "Wyoming": "Cheyenne"
}

BANNED = [str(i) for i in range(1, 32)] + ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"] + ["snow", "weather", "winter", "storm", "rainwinds", "mph", "cloudy", "copy", "link", "copyshortcut", "copied", "updated"]

BANNED_REV = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"] + ["snow", "weather", "winter", "storm", "rainwinds", "mph", "cloudy", "copy", "link", "copyshortcut", "copied", "updated", "news"]
