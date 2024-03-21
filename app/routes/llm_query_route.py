from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.classes.llm_assist import LLMAssistance
from app.classes.ticket_assignment import TicketAssignment
import random
from datetime import datetime


router = APIRouter()
llmAssistanceObj = LLMAssistance()
ticket_assigner = TicketAssignment()

technician_details = []
issue_type = ""
lati = 0.0
longi = 0.0

@router.get('/query')
async def ask_queries_returns_appropriate_technician_details(query: str = Query(..., title="query", description="Enter the query"),
                      lat: float = Query(..., title="latitude", description="Enter the latitude"),
                      long: float = Query(..., title="longitude", description="Enter the longitude")):
    response = llmAssistanceObj.get_technician_using_llm(question=query, user_lat=lat, user_lon=long)
    global technician_details, issue_type, lati, longi
    technician_details = response
    issue_type = query
    lati = lat
    longi = long
    return JSONResponse(content=response, status_code=200)


@router.post("/auto_assign_ticket")
async def auto_assign_ticket():
    global technician_details, lati,longi, issue_type  # Access the global variable
    ticket_id_prefix = "Tech"
    for technician in technician_details:
        if technician["day_schedule"] == "booked":
            continue
        else:
            tech_id = technician["_id"]
            break
    else:
        return JSONResponse(content="No Technician is free", status_code=400)
    
    current_time = datetime.now().strftime("%H%M%S%f")
    ticket_id = f"{ticket_id_prefix}{tech_id}{current_time}"
    
    response = ticket_assigner.auto_assign_ticket(ticket_id,tech_id,lati,longi,issue_type, urgency="High Urgency")
    return JSONResponse(content=response, status_code=200)

@router.post("/manual_assign_ticket")
async def manual_assign_ticket(technician_id: str = Query(..., title="Technician ID")):
    ticket_id_prefix = "Tech"
    tech_id = technician_id
    current_time = datetime.now().strftime("%H%M%S%f")
    ticket_id = f"{ticket_id_prefix}{tech_id}{current_time}"
    response = ticket_assigner.manual_assign_ticket(ticket_id, technician_id, issue_type, lati, longi, urgency="High Urgency")
    return JSONResponse(content=response, status_code=200)
