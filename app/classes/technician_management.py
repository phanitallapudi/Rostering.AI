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

    def format_phone_number(self, phoneno: str) -> str:
        if not phoneno.startswith("+91-"):
            phoneno = "+91-" + phoneno
        return phoneno

    def create_profile(self, username, profile: TechnicianProfile):
        user = user_data.find_one({"username": username})
        formatted_phoneno = self.format_phone_number(profile.phoneno)
        profile_data = {
            "name": profile.name,
            "skill_set": profile.skill_set,
            "rating" : 2.5,
            "feedback_sentiment": "neutral",
            "experience_years": profile.experience_years,
            "current_location": get_random_location(),
            "day_schedule": "free",
            "phoneno": formatted_phoneno,
            "user" : user["_id"]
        }
        result = technicians_info.insert_one(profile_data)
        if result:
            return {"message" : f"Created profile for {username} with profile name as {profile.name}"}
        return {"message" : f"Cannot able to create profile for {username}"}