from geopy.geocoders import Nominatim
from config import CAPITALS, MAP_FILE
import sqlite3

def get_publisher_latlong(city, state):
    if city is None:
        if state in CAPITALS:
         city = CAPITALS[state]
        return None
    query = city + "," + state if state else city
    geolocator = Nominatim(user_agent="newsm_hackathon_!/1.0")  # Provide a unique user agent
    location = geolocator.geocode(query)
    if location:
        return location.latitude, location.longitude
    else:
        return None  # Return None if the address could not be found
    
def get_coordinates(city, state):
    if city is None:
        if state in CAPITALS:
            city = CAPITALS[state]
        else:
            return None
    
    conn = sqlite3.connect(MAP_FILE)
    cursor = conn.cursor()
    if state is None:
        cursor.execute("SELECT latitude, longitude FROM cities WHERE city LIKE ? LIMIT 1", (f"%{city}%",))    
    else:
        cursor.execute("SELECT latitude, longitude FROM cities WHERE city LIKE ? AND state=?", (f"%{city}%", state))
    result = cursor.fetchone()
    conn.close()
    return result


