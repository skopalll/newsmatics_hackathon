from geopy.geocoders import Nominatim

def get_publisher_latlong(address):
    geolocator = Nominatim(user_agent="newsm_hackathon_!/1.0")  # Provide a unique user agent
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None  # Return None if the address could not be found

# Example usage:

lat, long = get_publisher_latlong("New York, New York")
if lat and long:
    print(f"Latitude: {lat}, Longitude: {long}")
else:
    print("Address not found.")