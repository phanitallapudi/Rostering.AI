from pymongo import DESCENDING
from app.classes.dbconfig import application_activity

class ActivityInfo:
    def __init__(self) -> None:
        pass

    def get_recent_activity(self):
        recent_entries = list(application_activity.find().sort("created_at", DESCENDING).limit(5))
        for entry in recent_entries:
            entry["_id"] = str(entry["_id"])
            entry["created_at"] = entry['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        return recent_entries