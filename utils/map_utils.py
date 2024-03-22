from geopy.geocoders import Nominatim
from app.classes.dbconfig import location_data
from sklearn.cluster import KMeans
from dotenv import load_dotenv

import numpy as np
import requests
import os

load_dotenv()

def get_address(latitude, longitude):
    geolocator = Nominatim(user_agent="location_finder")
    location = geolocator.reverse((latitude, longitude), language="en")
    return location.address

def get_cluster_id(location):
    query_result = location_data.find({}, {"_id": 0, "location": 1})
    locations_list = [entry["location"] for entry in query_result]
    
    kmeans = KMeans(n_clusters=10, random_state=42)
    kmeans.fit(locations_list)
    cluster_ids = kmeans.labels_

    cluster_id = kmeans.predict([location])[0]

    return int(cluster_id)

def get_random_location():
    latitude = np.random.uniform(12.957078201607976, 12.991691702207596)
    longitude = np.random.uniform(77.70729957027493, 77.74926821385183)
    return [latitude, longitude]

def calculate_route(origin: str, destination: str) -> dict:
    tom_tom_api_key = os.getenv("TOMTOM_KEY")

    origin = truncate_coordinates(origin)
    destination = truncate_coordinates(destination)
    
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{origin}:{destination}/json?sectionType=traffic&routeType=fastest&traffic=true&travelMode=motorcycle&key={tom_tom_api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to calculate route. Status code:", "status_code": response.status_code}
    
def truncate_coordinates(coordinates: str) -> str:
    lat, lon = coordinates.split(",")
    lat_truncated = "{:.5f}".format(float(lat))
    lon_truncated = "{:.5f}".format(float(lon))
    return f"{lat_truncated},{lon_truncated}"