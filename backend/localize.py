from geopy.geocoders import Nominatim
from config import CAPITALS

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

