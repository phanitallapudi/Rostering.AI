from geopy.geocoders import Nominatim

def get_address(latitude, longitude):
    geolocator = Nominatim(user_agent="location_finder")
    location = geolocator.reverse((latitude, longitude), language="en")
    return location.address