from pydantic import BaseModel
from datetime import datetime

class ActivityTags:
    modified = "modified"
    add = "add"
    prebook = "prebook"

class PrebookTechnician(BaseModel):
    technician_id: str
    start_time: datetime
    end_time: datetime
