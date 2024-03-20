import random
import csv
from sklearn.cluster import KMeans

12.979526794275344, 77.70969242872029
12.955149476845158, 77.74724762666868

def generate_coordinates(num_points, min_lat=12.979526794275344, max_lat=12.955149476845158, min_lon=77.70969242872029, max_lon=77.74724762666868):
    coordinates = []
    for _ in range(num_points):
        lat = random.uniform(min_lat, max_lat)
        lon = random.uniform(min_lon, max_lon)
        coordinates.append((lat, lon))
    return coordinates

coordinates = generate_coordinates(50)

# K-means clustering
kmeans = KMeans(n_clusters=20, random_state=42)
kmeans.fit(coordinates)
cluster_ids = kmeans.labels_

# Save clusters to CSV file
with open('clusters.csv', 'w', newline='') as csvfile:
    fieldnames = ['location', 'cluster_id', 'times_used']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for idx, coord in enumerate(coordinates):
        cluster_id = cluster_ids[idx]
        x = [coord[0], coord[1]]
        writer.writerow({'location' : x, 'cluster_id': cluster_id, 'times_used' : 0})

print("CSV file 'clusters.csv' generated successfully.")
