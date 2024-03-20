from fastapi import APIRouter, Query, HTTPException, Depends, Request, status
from app.classes.login import get_current_user, authorize_user, authorize_both_user, oauth2_scheme, User
from app.classes.ticket_management import TicketManagement, Ticket
from fastapi.responses import JSONResponse

router = APIRouter()
ticketManagerObj = TicketManagement()
auto_assign_active = True

@router.get("/auto_assign_status", dependencies=[Depends(authorize_user)])
async def get_auto_toggle_status(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    resposne = {"status": auto_assign_active }
    return JSONResponse(content=resposne, status_code=200)

@router.post("/auto_assign_toggle/{status}", dependencies=[Depends(authorize_user)])
async def toggle_auto_assign(status: bool, current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    global auto_assign_active
    auto_assign_active = status
    return {"message": f"Auto-assign feature is {'enabled' if status else 'disabled'}"}

@router.post("/create_ticket", dependencies=[Depends(authorize_user)])
async def create_ticket(ticket: Ticket, current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    response = ticketManagerObj.create_ticket(ticket=ticket, auto_assign=auto_assign_active)
    return JSONResponse(content=response, status_code=200)

@router.get("/all_tickets", dependencies=[Depends(authorize_user)])
async def get_all_generated_tickets(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    response = ticketManagerObj.get_all_tickets()
    return JSONResponse(content=response, status_code=200)

@router.get("/get_single_ticket", dependencies=[Depends(authorize_user)])
async def get_single_ticket(_id: str = Query(..., title="data", description="Enter the _id of the ticket"), 
                            current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    response = ticketManagerObj.get_single_ticket(_id)
    return JSONResponse(content=response, status_code=200)