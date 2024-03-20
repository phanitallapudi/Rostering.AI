from geopy.geocoders import Nominatim
from app.classes.dbconfig import location_data
from sklearn.cluster import KMeans
import numpy as np

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

    return cluster_id

def get_random_location():
    latitude = np.random.uniform(12.957078201607976, 12.991691702207596)
    longitude = np.random.uniform(77.70729957027493, 77.74926821385183)
    return [latitude, longitude]