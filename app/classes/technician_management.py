from app.classes.dbconfig import user_data, technicians_info
from utils.map_utils import get_address, get_random_location, get_cluster_id
from utils.database_utils import generate_unique_id, parse_excel_or_csv
from app.classes.technicians_info import TechniciansInfo
from pydantic import BaseModel, field_validator
import random

class TechnicianProfile(BaseModel):
    name: str
    skill_set: str
    experience_years: int
    phoneno: str

class TechnicianManagement(TechniciansInfo):
    def __init__(self) -> None:
        pass

    def format_phone_number(self, phoneno: str) -> str:
        if not phoneno.startswith("+91-"):
            phoneno = "+91-" + phoneno
        return phoneno

    def create_profile(self, username, profile: TechnicianProfile):
        user = user_data.find_one({"username": username})
        if not user:
            return {"message": f"User '{username}' not found."}

        profile_data = technicians_info.find_one({"user" : user["_id"]})

        if profile_data:
            return {"message" : f"profile for {username} already exists, please update it."}
        formatted_phoneno = self.format_phone_number(profile.phoneno)

        location = get_random_location() #needs to get it from the user

        while True:
            uid = generate_unique_id()
            if not technicians_info.find_one({"uid": uid}):
                break

        address = get_address(location[0], location[1])
        
        profile_data = {
            "uid" : uid,
            "name": profile.name,
            "skill_set": profile.skill_set,
            "rating" : 2.5,
            "feedback_sentiment": "neutral",
            "experience_years": profile.experience_years,
            "current_location": location,
            "address": address,
            "day_schedule": "free",
            "phoneno": formatted_phoneno,
            "user" : user["_id"],
            "cluster_id" : int(get_cluster_id(location))
        }
        result = technicians_info.insert_one(profile_data)
        if result:
            return {"message" : f"Created profile for {username} with profile name as {profile.name}"}
        return {"message" : f"Cannot able to create profile for {username}"}
    
    def upload_csv_file(self, file):
        df = parse_excel_or_csv(file)
        
        generated_uids = set(df['uid'])
        existing_uids = set(technicians_info.distinct('uid'))  # Assuming 'uid' is the field name in MongoDB
        
        new_uids = generated_uids.difference(existing_uids)
        new_uids = new_uids.union({generate_unique_id() for _ in range(len(generated_uids) - len(new_uids))})
        
        id_mapping = dict(zip(generated_uids, new_uids))
        df['uid'] = df['uid'].map(id_mapping)

        # Convert DataFrame to dictionary for MongoDB insertion
        data = df.to_dict(orient='records')
        # Insert data into MongoDB
        result = technicians_info.insert_many(data)
        num_entries = len(result.inserted_ids)

        self.update_cluster_id_technician()    
        return {"message": f"File uploaded successfully. {num_entries} entries inserted into MongoDB"}