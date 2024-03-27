from bson import ObjectId
from app.classes.dbconfig import technicians_info
from utils.map_utils import get_address, get_cluster_id
from math import radians, sin, cos, sqrt, atan2

class TechniciansInfo:
    def __init__(self) -> None:
        pass

    def get_all_technicians(self):
        technicians = list(technicians_info.find({}))
        for technician in technicians:
            technician['_id'] = str(technician['_id'])
            user_id = technician.get('user')
            if user_id:
                technician['user'] = str(user_id)
        return technicians
    
    def get_all_technicians_skills(self, skill_set):
        query = {"skill_set": skill_set}
        technicians = list(technicians_info.find(query))
        for technician in technicians:
            technician['_id'] = str(technician['_id'])
            user_id = technician.get('user')
            if user_id:
                technician['user'] = str(user_id)
        return technicians
    
    def get_all_technicians_skills_clusterid(self, skill_set, cluster_id):
        query = {"skill_set": skill_set, "cluster_id": cluster_id}
        technicians = list(technicians_info.find(query))
        for technician in technicians:
            technician['_id'] = str(technician['_id'])
            user_id = technician.get('user')
            if user_id:
                technician['user'] = str(user_id)
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
    
    def find_nearest_persons(self, latitude, longitude, technicians_list, num_persons=5):
        """
        Find the top 'num_persons' nearest persons with the required skill_set,
        based on the given latitude and longitude.
        """
        # Calculate distances to all technicians with the required skill_set
        distances = []
        for technician in technicians_list:
            tech_lat, tech_lon = technician['current_location']
            distance = self.calculate_distance(latitude, longitude, tech_lat, tech_lon)
            
            if technician['feedback_sentiment'] == "positive":
                experience_weight = 1
                
            elif technician['feedback_sentiment'] == "neutral":
                experience_weight = 0
                
            else:
                experience_weight = -1
                
            if technician["day_schedule"] == "free":
                schedule = 1
            else:
                schedule = 0
                
            rating_weight = technician['rating'] * (100 / 3)
            feedback_weight = technician['experience_years'] * (100 / 3)
            experience_weight = experience_weight * (100 / 3)
            weightage_score = rating_weight + feedback_weight + experience_weight
            
            distances.append((technician, distance, weightage_score, schedule))

        # Sort the list of distances by distance
        sorted_distances = sorted(distances, key=lambda x: (-x[3], x[1], -x[2]))

        # Extract top 'num_persons' nearest persons
        top_persons = []
        for i in range(min(num_persons, len(sorted_distances))):
            person, distance, weightage_score , schedule = sorted_distances[i]
            top_persons.append(person)

        for person in top_persons:
            lat, long = person["current_location"]
            location_details = get_address(latitude=lat, longitude=long)
            person["location_details"] = location_details

        return top_persons
      
    def get_single_technician(self, _id):
        _id = ObjectId(_id)
        # Perform the query
        ticket = technicians_info.find_one({"_id": _id})
        ticket["_id"] = str(ticket["_id"])
        return ticket
    
    def get_nearest_technician(self, user_lat, user_lon, skill_set):
        user_location = (user_lat, user_lon)
        cluster_id = int(get_cluster_id(user_location))
        technicians_list = self.get_all_technicians_skills_clusterid(skill_set=skill_set, cluster_id=cluster_id)
        nearest_persons = self.find_nearest_persons(latitude=user_lat, longitude=user_lon, technicians_list=technicians_list, num_persons=5)
        return nearest_persons

    def update_cluster_id_technician(self):
        cluster_column = "cluster_id"
        updated_count = 0
        for entry in technicians_info.find({cluster_column: {"$exists": False}}):  # Only get entries without the new column
            location = entry["current_location"]
            retrieved_cluster_id = get_cluster_id(location)
            response = technicians_info.update_one({"_id": entry["_id"]}, {"$set": {cluster_column: int(retrieved_cluster_id)}})
            if response.modified_count > 0:
                updated_count += 1
        return {"response": f"{updated_count} documents updated."}
    
    def update_technician_address(self):
        address_column = "address"
        updated_count = 0
        for entry in technicians_info.find({address_column: {"$exists": False}}):
            location = entry["current_location"]
            updated_address = get_address(location[0], location[1])  
            response = technicians_info.update_one(
                {"_id": entry["_id"]}, 
                {"$set": {address_column: updated_address}},
                upsert=False 
            )
            if response.modified_count > 0:
                updated_count += 1
        return {"response": f"{updated_count} documents updated."}
