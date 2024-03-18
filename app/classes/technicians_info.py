from app.classes.dbconfig import technicians_info
from math import radians, sin, cos, sqrt, atan2

class TechniciansInfo:
    def __init__(self) -> None:
        pass

    def get_all_technicians(self):
        technicians = list(technicians_info.find({}))
        for technician in technicians:
            technician['_id'] = str(technician['_id'])
        return technicians
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the distance between two points on the Earth's surface
        using the Haversine formula.
        """
        # Radius of the Earth in kilometers
        R = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)

        # Difference between latitudes and longitudes
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine formula
        a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Calculate the distance
        distance = R * c

        return distance
    
    def find_nearest_persons(self, latitude, longitude, skill_set, technicians_list, num_persons=5):
        """
        Find the top 'num_persons' nearest persons with the required skill_set,
        based on the given latitude and longitude.
        """
        # Calculate distances to all technicians with the required skill_set
        distances = []
        for technician in technicians_list:
            if technician['skill_set'] == skill_set:
                tech_lat, tech_lon = technician['current_location']
                distance = self.calculate_distance(latitude, longitude, tech_lat, tech_lon)
                distances.append((technician, distance))

        # Sort the list of distances by distance
        sorted_distances = sorted(distances, key=lambda x: x[1])

        # Extract top 'num_persons' nearest persons
        top_persons = []
        for i in range(min(num_persons, len(sorted_distances))):
            person, distance = sorted_distances[i]
            top_persons.append(person)

        return top_persons
    
    def get_nearest_technician_skillset(self, user_lat, user_lon, skill_set):
        technicians_list = self.get_all_technicians()
        nearest_persons = self.find_nearest_persons(latitude=user_lat, longitude=user_lon, skill_set=skill_set, technicians_list=technicians_list, num_persons=5)
        return nearest_persons

