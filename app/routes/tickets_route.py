from fastapi import APIRouter, Query, HTTPException, Depends, Request, status
from app.classes.login import get_current_user, authorize_user, authorize_both_user, oauth2_scheme, User
from app.classes.ticket_management import TicketManagement, Ticket
from fastapi.responses import JSONResponse

router = APIRouter()
ticketManagerObj = TicketManagement()
auto_assign_active = False

@router.get("/auto_assign_status", dependencies=[Depends(authorize_user)])
async def get_auto_toggle_status(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Retrieves the status of automatic technician assignment toggling.

    This endpoint allows an admin user to retrieve the current status of automatic technician assignment toggling. Authentication is required via OAuth2 token, and only users with the "Admin" role are allowed to access this endpoint. If the user does not have the appropriate permissions, it returns a 401 Unauthorized error. Upon successful authorization, it returns the current status of automatic assignment toggling as a JSON response with a status code of 200.
    
    **Returns:**
    - `dict`: A dictionary containing the status of automatic assignment toggling.
    """
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    resposne = {"status": auto_assign_active }
    return JSONResponse(content=resposne, status_code=200)

@router.post("/auto_assign_toggle/{status}", dependencies=[Depends(authorize_user)])
async def toggle_auto_assign(status: bool, current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Toggles the automatic technician assignment feature.

    This endpoint allows an admin user to toggle the automatic technician assignment feature on or off by providing a boolean value in the URL path. Authentication is required via OAuth2 token, and only users with the "Admin" role are allowed to access this endpoint. If the user does not have the appropriate permissions, it returns a 401 Unauthorized error. Upon successful authorization, it toggles the status of the automatic assignment feature based on the provided boolean value and returns a message confirming the action.
    
    **URL Path Parameters:**
    - `status` (bool): The boolean value indicating whether to enable (True) or disable (False) the automatic assignment feature.
    
    **Returns:**
    - `dict`: A dictionary containing a message confirming the status of the automatic assignment feature.
    """
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    global auto_assign_active
    auto_assign_active = status
    return {"message": f"Auto-assign feature is {'enabled' if status else 'disabled'}"}

@router.post("/create_ticket", dependencies=[Depends(authorize_user)])
async def create_ticket(ticket: Ticket, current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Creates a new ticket.

    This endpoint allows an admin user to create a new ticket by providing ticket details in the request body. Authentication is required via OAuth2 token, and only users with the "Admin" role are allowed to access this endpoint. Upon receiving the request, the endpoint creates a new ticket using the provided details and the current status of the automatic assignment feature. It then returns the response containing information about the created ticket as a JSON response with a status code of 200.
    
    **Request Body (JSON):**
    - `ticket` (Ticket): The details of the ticket to be created.
    
    **Returns:**
    - `dict`: A dictionary containing information about the created ticket.
    """
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    response = ticketManagerObj.create_ticket(ticket=ticket, auto_assign=auto_assign_active)
    return JSONResponse(content=response, status_code=200)

@router.put("/assign_ticket", dependencies=[Depends(authorize_user)])
async def assign_ticket_manually_to_technician(ticket_id: str, technician_id: str,
                                               current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Manually assigns a ticket to a technician.

    This endpoint allows an admin user to manually assign a ticket to a technician by providing the ticket ID and technician ID in the request parameters. Authentication is required via OAuth2 token, and only users with the "Admin" role are allowed to access this endpoint. Upon successful authorization, the endpoint assigns the specified ticket to the specified technician and returns a JSON response with a status code of 200.

    **Parameters:**
    - `ticket_id` (str): The ID of the ticket to be assigned.
    - `technician_id` (str): The ID of the technician to whom the ticket will be assigned.

    **Returns:**
    - `dict`: A dictionary containing information about the assignment.
    """
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = ticketManagerObj.assign_ticket_manually(ticket_id=ticket_id, technician_id=technician_id)
    return JSONResponse(content=response, status_code=200)

@router.get("/all_tickets", dependencies=[Depends(authorize_user)])
async def get_all_generated_tickets(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Retrieves all generated tickets.

    This endpoint allows an admin user to retrieve all generated tickets. Authentication is required via OAuth2 token, and only users with the "Admin" role are allowed to access this endpoint. Upon successful authorization, the endpoint retrieves all generated tickets from the ticket manager and returns them as a JSON response with a status code of 200.
    
    **Returns:**
    - `dict`: A dictionary containing information about all generated tickets.
    """
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    response = ticketManagerObj.get_all_tickets()
    return JSONResponse(content=response, status_code=200)

@router.get("/get_single_ticket", dependencies=[Depends(authorize_user)])
async def get_single_ticket(_id: str = Query(..., title="data", description="Enter the _id of the ticket"), 
                            current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Retrieves information about a single ticket.

    This endpoint allows an admin user to retrieve information about a single ticket by providing its unique identifier (_id). Authentication is required via OAuth2 token, and only users with the "Admin" role are allowed to access this endpoint. Upon receiving the request, the endpoint fetches information about the specified ticket from the ticket manager based on its _id and returns it as a JSON response with a status code of 200.
    
    **Query Parameters:**
    - `_id` (str): The unique identifier of the ticket.
    
    **Returns:**
    - `dict`: A dictionary containing information about the specified ticket.
    """
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    response = ticketManagerObj.get_single_ticket(_id)
    return JSONResponse(content=response, status_code=200)

@router.get("/information", dependencies=[Depends(authorize_user)])
async def get_information_about_ticket_status(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    response = ticketManagerObj.get_status_all_ticket()
    return JSONResponse(content=response, status_code=200)
