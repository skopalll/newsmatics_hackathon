from geopy.geocoders import Nominatim

def get_publisher_latlong(cityandstate):
    geolocator = Nominatim(user_agent="newsm_hackathon_!/1.0")  # Provide a unique user agent
    location = geolocator.geocode(cityandstate)
    if location:
        return location.latitude, location.longitude
    else:
        return None  # Return None if the address could not be found

