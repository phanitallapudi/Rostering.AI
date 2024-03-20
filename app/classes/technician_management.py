from app.classes.dbconfig import user_data, technicians_info
from utils.map_utils import get_random_location
from pydantic import BaseModel, field_validator

class TechnicianProfile(BaseModel):
    name: str
    skill_set: str
    experience_years: int
    phoneno: str

class TechnicianManagement:
    def __init__(self) -> None:
        pass

    def create_profile(self, username, profile: TechnicianProfile):
        user = user_data.find_one({"username": username})
        print(user)
        profile_data = {
            "name": profile.name,
            "skill_set": profile.skill_set,
            "rating" : None,
            "feedback_sentiment": None,
            "experience_years": profile.experience_years,
            "current_location": get_random_location(),
            "day_schedule": "free",
            "phoneno": profile.phoneno,
            "user" : user["_id"]
        }
        result = technicians_info.insert_one(profile_data)
        if result:
            return True
        return False