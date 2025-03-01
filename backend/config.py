import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "log.txt")
DB_FILE = os.path.join(os.path.dirname(__file__), "data", "sqlite.db")
MAP_FILE = os.path.join(os.path.dirname(__file__), "data", "cities.db")
API_BASE_URL = "https://www.newsmatics.com/news-index"
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NDA0MDAxMTgsInN1YiI6NDMyLCJleHAiOjIwNTU3NjAxMTguMCwic2NvcGVzIjpbImFsbCJdfQ.ZgWINtJswrrJGeVH0GrDG7LZGgv57Y5anU6YBag9edo" 

KEYWORDS = {
    "politics": [
        "elections", "government", "parliament", "senate", "congress",
        "president", "political party", "policy", "legislation", "democracy",
        "campaign", "diplomacy", "lobbying", "voting", "geopolitics"
    ],
    "science": [
        "physics", "chemistry", "biology", "astronomy", "genetics",
        "neuroscience", "quantum mechanics", "space exploration", "NASA",
        "climate change", "AI in science", "CRISPR", "evolution", "robotics",
        "scientific research"
    ],
    "it": [
        "artificial intelligence", "cybersecurity", "blockchain", "quantum computing",
        "cloud computing", "5G", "software development", "data science",
        "machine learning", "internet of things", "big data", "hacking",
        "digital transformation", "metaverse", "deep learning"
    ],
    "breaking_news": [
        "emergency", "breaking news", "urgent", "crisis", "disaster",
        "evacuation", "protest", "riot", "hostage", "wildfire",
        "earthquake", "hurricane", "tornado", "tsunami", "explosion"
    ],
    "killings_and_crashes": [
        "murder", "homicide", "shooting", "massacre", "assassination",
        "terrorist attack", "car crash", "plane crash", "train derailment",
        "fatal accident", "gun violence", "police shooting", "hit and run",
        "bombing", "vehicular manslaughter"
    ],
    "economics": [
        "inflation", "recession", "stock market", "GDP", "economic policy",
        "interest rates", "trade war", "financial crisis", "banking",
        "cryptocurrency", "investments", "unemployment", "real estate market",
        "federal reserve", "business cycle"
    ]
}

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