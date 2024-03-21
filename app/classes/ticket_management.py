from app.classes.dbconfig import user_data, tickets_data, technicians_info
from utils.map_utils import get_random_location, get_cluster_id
from utils.database_utils import generate_unique_id
from app.classes.technicians_info import TechniciansInfo
from pydantic import BaseModel, field_validator
from bson import ObjectId

class Ticket(BaseModel):
    title: str
    description: str
    status: str = "open"
    priority: int = 1
    location: list[float] = get_random_location()

    @field_validator('title')
    def validate_title(cls, v):
        allowed_titles = ["router setup", "cable repair", "software troubleshooting", "fiber optics", "customer service"]
        if v not in allowed_titles:
            raise ValueError(f"Title must be one of: {', '.join(allowed_titles)}")
        return v

class TicketManagement(TechniciansInfo):
    def __init__(self) -> None:
        pass

    def create_ticket(self, ticket: Ticket, auto_assign):
        def generate_unique_ticket_id():
            while True:
                uid = generate_unique_id()
                if not tickets_data.find_one({"uid": uid}):
                    return uid

        coordinates = ticket.location
        ticket_information = {
            "uid": generate_unique_ticket_id(),
            "title": ticket.title,
            "description": ticket.description,
            "status": ticket.status,
            "priority": ticket.priority,
            "assigned_to": None,
            "location": ticket.location
        }

        if auto_assign:
            matches_technician = self.get_nearest_technician(user_lat=coordinates[0], user_lon=coordinates[1], skill_set=ticket.title)

            if not matches_technician:
                tickets_data.insert_one(ticket_information)
                return {"message": f"No matching technician found. Ticket #{ticket_information['uid']} sent for manual assignment."}

            top_technician = matches_technician[0]
            technician_id = ObjectId(top_technician["_id"])
            ticket_information["assigned_to"] = technician_id
            technicians_info.update_one({"_id": technician_id}, {"$set": {"day_schedule": "booked"}})

        result = tickets_data.insert_one(ticket_information)
        if result:
            return {"message": f"Created ticket with id: {ticket_information['uid']}"}
        return {"message": f"Cannot able to create ticket"}

    def get_all_tickets(self):
        tickets = list(tickets_data.find({}))
        for ticket in tickets:
            ticket['_id'] = str(ticket['_id'])
            user_id = ticket.get('assigned_to')
            if user_id:
                ticket['assigned_to'] = str(user_id)
        return tickets
    
    def get_single_ticket(self, _id):
        _id = ObjectId(_id)
        # Perform the query
        ticket = tickets_data.find_one({"_id": _id})
        ticket["_id"] = str(ticket["_id"])
        user_id = ticket.get('assigned_to')
        if user_id:
            technician = technicians_info.find_one({"_id": user_id})
            technician["_id"] = str(technician["_id"])
            ticket['assigned_to'] = technician
        return ticket

    
