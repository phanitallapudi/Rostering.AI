from bson import ObjectId
from app.classes.dbconfig import technicians_info, application_activity
from app.classes.models import ActivityTags
from utils.map_utils import get_address, get_cluster_id
from math import radians, sin, cos, sqrt, atan2
from heapq import nlargest
from datetime import datetime, timedelta

import pytz

class TechniciansInfo:
    def __init__(self) -> None:
        self.IST = pytz.timezone('Asia/Kolkata')

    def get_all_technicians(self):
        technicians = list(technicians_info.find({}))
        for technician in technicians:
            technician['_id'] = str(technician['_id'])
            user_id = technician.get('user')
            start_date = technician.get("start_date")
            end_date = technician.get("end_date")

            # Format dates if they exist
            if start_date != None:
                technician['start_date'] = start_date.strftime("%Y-%m-%d %H:%M:%S")
            if end_date != None:
                technician['end_date'] = end_date.strftime("%Y-%m-%d %H:%M:%S")
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
    
    def get_top5_technicians(self):
        skill_sets = technicians_info.distinct("skill_set")
        top_technicians = {}

        for skill in skill_sets:
            technicians = technicians_info.find({"skill_set": skill})
            top_5 = nlargest(5, technicians, key=lambda x: (x['rating'], 1 if x['feedback_sentiment'] == 'positive' else 0))
            top_technicians[skill] = [technician['name'] for technician in top_5]

        return top_technicians
    
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
                schedule = 2
            elif technician['day_schedule'] == "standby":
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
            
            start_date = person.get("start_date")
            end_date = person.get("end_date")
            
            # Format dates if they exist
            if start_date != None:
                person['start_date'] = start_date.strftime("%Y-%m-%d %H:%M:%S")
            if end_date != None:
                person['end_date'] = end_date.strftime("%Y-%m-%d %H:%M:%S")

            top_persons.append(person)
            

        # for person in top_persons:
        #     lat, long = person["current_location"]
        #     location_details = get_address(latitude=lat, longitude=long)
        #     person["location_details"] = location_details

        return top_persons
      
    def get_single_technician(self, _id):
        _id = ObjectId(_id)
        # Perform the query
        person = technicians_info.find_one({"_id": _id})
        person["_id"] = str(person["_id"])
        start_date = person.get("start_date")
        end_date = person.get("end_date")
        
        # Format dates if they exist
        if start_date != None:
            person['start_date'] = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if end_date != None:
            person['end_date'] = end_date.strftime("%Y-%m-%d %H:%M:%S")
        return person
    
    def get_nearest_technician(self, user_lat, user_lon, skill_set):
        user_location = (user_lat, user_lon)
        cluster_id = int(get_cluster_id(user_location))
        technicians_list = self.get_all_technicians_skills_clusterid(skill_set=skill_set, cluster_id=cluster_id)
        nearest_persons = self.find_nearest_persons(latitude=user_lat, longitude=user_lon, technicians_list=technicians_list, num_persons=5)
        return nearest_persons

    def update_cluster_id_technician(self):
        cluster_column = "cluster_id"
        updated_count = 0
        #for entry in technicians_info.find({cluster_column: {"$exists": False}}):
        for entry in technicians_info.find():  # Only get entries without the new column
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
    
        
    def prebook_technician(self, technician_id, start_date, end_date, username):
        technician = technicians_info.find_one({"_id" : ObjectId(technician_id)})

        if technician is None:
            return {"message": f"No technician found with this _id {technician_id}"}
        
        if technician["day_schedule"] == "booked":
            return {"message": f"Technician with _id {technician['uid']} is already booked"}
        
        result = technicians_info.update_one(
        {"_id": ObjectId(technician_id)},
        {
            "$set": {
                "day_schedule": "standby",
                "start_date": start_date,
                "end_date": end_date
            }
        }
    )
        if result:
            activity_entry = f"{username} pre-booked technician with uid {technician['uid']} from {start_date.strftime('%Y-%m-%d %H:%M:%S')} to {end_date.strftime('%Y-%m-%d %H:%M:%S')}"
            tag = ActivityTags.modified
            current_time = datetime.now(self.IST)

            activity_info = {
                "activity": activity_entry,
                "tag": tag,
                "created_at": current_time 
            }

            application_activity.insert_one(activity_info)
            return {"message": f"Technician with uid {technician['uid']} assigned to standby successfully"}
        return {"error": "Unable to book the technician"}
