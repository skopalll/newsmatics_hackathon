from geopy.geocoders import Nominatim
from config import CAPITALS
import sqlite3

def get_publisher_latlong(city, state):
    if city is None:
        city = CAPITALS[state]
    query = city + "," + state if state else city
    geolocator = Nominatim(user_agent="newsm_hackathon_!/1.0")  # Provide a unique user agent
    location = geolocator.geocode(query)
    if location:
        return location.latitude, location.longitude
    else:
        return None  # Return None if the address could not be found
    
def get_coordinates(city, state, db_file="../database/us_cities.db"):
    if city is None:
        city = CAPITALS[state]
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    if state is None:
        cursor.execute("SELECT latitude, longitude FROM cities WHERE city=? LIMIT 1", (city))    
    else:
        cursor.execute("SELECT latitude, longitude FROM cities WHERE city=? AND state=?", (city, state))
    result = cursor.fetchone()
    conn.close()
    return result


