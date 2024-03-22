import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TOMTOM_KEY")

def calculate_route(origin: str, destination: str) -> dict:
    origin = truncate_coordinates(origin)
    destination = truncate_coordinates(destination)
    
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{origin}:{destination}/json?sectionType=traffic&routeType=fastest&traffic=true&travelMode=motorcycle&key={API_KEY}"
    
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
