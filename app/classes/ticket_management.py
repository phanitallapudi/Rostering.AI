from app.classes.dbconfig import user_data, tickets_data
from utils.map_utils import get_random_location, get_cluster_id
from utils.database_utils import generate_unique_id
from pydantic import BaseModel, field_validator
from bson import ObjectId

class Ticket(BaseModel):
    title: str
    description: str
    status: str = "open"
    priority: int = 1

class TicketManagement:
    def __init__(self) -> None:
        pass

    def create_ticket(self, ticket: Ticket, auto_assign):
        if auto_assign:
            pass # write auto assign logic here
        while True:
            uid = generate_unique_id()
            if not tickets_data.find_one({"uid": uid}):
                break

        ticket_information = {
            "uid" : uid,
            "title": ticket.title,
            "description": ticket.description,
            "status": ticket.status,
            "priority": ticket.priority,
            "assigned_to": None
        }
        result = tickets_data.insert_one(ticket_information)

        if result:
            return {"message" : f"Created ticket with id: {uid}"}
        return {"message" : f"Cannot able to create ticket"}

    def get_all_tickets(self):
        tickets = list(tickets_data.find({}))
        for ticket in tickets:
            ticket['_id'] = str(ticket['_id'])
            user_id = ticket.get('user')
            if user_id:
                ticket['user'] = str(user_id)
        return tickets
    
    def get_single_ticket(self, _id):
        _id = ObjectId(_id)
        # Perform the query
        ticket = tickets_data.find_one({"_id": _id})
        ticket["_id"] = str(ticket["_id"])
        user_id = ticket.get('user')
        if user_id:
            ticket['user'] = str(user_id)
        return ticket

    
