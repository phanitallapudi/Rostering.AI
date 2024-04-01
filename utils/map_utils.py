from geopy.geocoders import Nominatim
from app.classes.dbconfig import location_data
from sklearn.cluster import KMeans
from dotenv import load_dotenv

import numpy as np
import json
import urllib3
import requests
import os

load_dotenv()
urllib3.disable_warnings()

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
    
    # url = f"https://api.tomtom.com/routing/1/calculateRoute/{origin}:{destination}/json?sectionType=traffic&routeType=fastest&traffic=true&travelMode=motorcycle&key={tom_tom_api_key}"

    url = f"https://api.tomtom.com/routing/1/calculateRoute/{origin}:{destination}/json?computeTravelTimeFor=all&sectionType=traffic&report=effectiveSettings&routeType=fastest&traffic=true&travelMode=motorcycle&vehicleMaxSpeed=80&vehicleCommercial=false&vehicleEngineType=combustion&constantSpeedConsumptionInLitersPerHundredkm=40%2C3&currentFuelInLiters=5&key={tom_tom_api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to calculate route. Status code:", "status_code": response.status_code}
    
def get_weather_data(destination: str):
    weather_api_key = os.getenv("WEATHER_KEY")

    lat_truncated, lon_truncated = truncate_weather_coordinates(destination)
    latitude = lat_truncated
    longitude = lon_truncated

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={weather_api_key}&units=metric"
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        return json.dumps(response.json(), indent=4)
    else:
        print("Error:", response.status_code)
        return None

def truncate_coordinates(coordinates: str) -> str:
    lat, lon = coordinates.split(",")
    lat_truncated = "{:.5f}".format(float(lat))
    lon_truncated = "{:.5f}".format(float(lon))
    return f"{lat_truncated},{lon_truncated}"

def truncate_weather_coordinates(coordinates: str) -> tuple:
    lat, lon = coordinates.split(",")
    lat_truncated = "{:.5f}".format(float(lat))
    lon_truncated = "{:.5f}".format(float(lon))
    return lat_truncated, lon_truncated
