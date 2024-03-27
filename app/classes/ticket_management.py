from app.classes.dbconfig import user_data, tickets_data, technicians_info
from utils.map_utils import get_random_location, get_cluster_id
from utils.database_utils import generate_unique_id
from app.classes.technicians_info import TechniciansInfo
from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta
from bson import ObjectId

import pytz

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
        self.IST = pytz.timezone('Asia/Kolkata')

    def create_ticket(self, ticket: Ticket, auto_assign):
        def generate_unique_ticket_id():
            while True:
                uid = generate_unique_id()
                if not tickets_data.find_one({"uid": uid}):
                    return uid

        coordinates = ticket.location
        current_time = datetime.now(self.IST)

        ticket_information = {
            "uid": generate_unique_ticket_id(),
            "title": ticket.title,
            "description": ticket.description,
            "status": ticket.status,
            "priority": ticket.priority,
            "assigned_to": None,
            "location": ticket.location,
            "created_at": current_time
        }

        if auto_assign:
            matches_technician = self.get_nearest_technician(user_lat=coordinates[0], user_lon=coordinates[1], skill_set=ticket.title)

            if not matches_technician:
                tickets_data.insert_one(ticket_information)
                return {"message": f"No matching technician found. Ticket #{ticket_information['uid']} sent for manual assignment."}

            top_technician = matches_technician[0]
            technician_id = ObjectId(top_technician["_id"])
            ticket_information["assigned_to"] = technician_id
            ticket_information["status"] = "assigned"
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
            ticket['created_at'] = ticket['created_at'].strftime("%Y-%m-%d %H:%M:%S")
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

    def assign_ticket_manually(self, ticket_id, technician_id):
        ticket = tickets_data.find_one({"_id" : ObjectId(ticket_id)})
        ticket["_id"] = str(ticket["_id"])
        assigned_to = ticket.get('assigned_to')

        if str(assigned_to) == technician_id:
            return {"message": f"Ticket {ticket_id} is already assigned to {technician_id}"}

        assigned_technician = technicians_info.find_one({"_id": ObjectId(technician_id)})
        if not assigned_technician:
            return {"message": f"No technician found with {technician_id}"}
        if assigned_technician["day_schedule"] == "booked":
            return {"message": f"Technician with {technician_id} is not available"}

        if assigned_to:
            assigned_technician = technicians_info.find_one({"_id": ObjectId(assigned_to)})
            technicians_info.update_one({"_id": ObjectId(assigned_to)}, {"$set": {"day_schedule": "free"}})

        tickets_data.update_one({"_id" : ObjectId(ticket_id)}, {"$set": {"assigned_to": ObjectId(technician_id), "status": "assigned"}})
        technicians_info.update_one({"_id": ObjectId(technician_id)}, {"$set": {"day_schedule": "booked"}})

        return {"message": f"Assigned technician {technician_id} to ticket {ticket_id}"}
    
    def get_status_all_ticket(self):
        pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            {"$project": {"status": "$_id", "count": 1, "_id": 0}}
        ]

        ist = pytz.timezone('Asia/Kolkata')
        twenty_four_hours_ago = datetime.now(ist) - timedelta(hours=24)

        new_tickets_query = {"created_at": {"$gte": twenty_four_hours_ago}}
        new_tickets = list(tickets_data.find(new_tickets_query))

        ticket_counts = list(tickets_data.aggregate(pipeline))

        json_response = {}
        for ticket_count in ticket_counts:
            json_response[ticket_count["status"]] = ticket_count["count"]
        json_response["new_tickets_24hrs"] = len(new_tickets)

        return json_response

