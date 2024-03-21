from app.classes.dbconfig import technicians_info, ticket_info  # Import ticket_info collection
from app.classes.llm_assist import LLMAssistance
from utils.map_utils import get_address
from datetime import datetime
import random

class TicketAssignment:
    def __init__(self):
        pass

    def auto_assign_ticket(self, ticket_id, tech_id, lati, longi, issue_type, urgency):
        
        # Update technician's schedule to "booked"
        technicians_info.update_one({"technician_id": tech_id}, {"$set": {"day_schedule": "booked"}})
        
        # Update ticket information in the database
        ticket_info.insert_one({
            "ticket_id": ticket_id,
            "technician_id": tech_id,
            "issue_type": issue_type,
            "urgency": urgency,
            "current_location": (lati, longi),
            "assigned_time": datetime.now()
        })
        
        return f"Ticket {ticket_id} assigned to Technician {tech_id}."

    def manual_assign_ticket(self, ticket_id, technician_id, issue_type, lati, longi, urgency):
        # Update technician's schedule to "booked"
        technicians_info.update_one({"technician_id": technician_id}, {"$set": {"day_schedule": "booked"}})
        
        # Update ticket information in the database
        ticket_info.insert_one({
            "ticket_id": ticket_id,
            "technician_id": technician_id,
            "issue_type": issue_type,
            "urgency": urgency,
            "current_location": (lati, longi),
            "assigned_time": datetime.now()
        })
        
        return f"Ticket {ticket_id} manually assigned to Technician {technician_id}."

   