from fastapi import APIRouter, Query, HTTPException, Depends, Request, status
from app.classes.login import get_current_user, authorize_user, authorize_both_user, oauth2_scheme, User
from app.classes.data_vizualization import DataVizualizer
from fastapi.responses import JSONResponse

router = APIRouter()
dataVizualizerObj = DataVizualizer()

@router.get("/get_infographics_technicians", dependencies=[Depends(authorize_user)])
async def get_infographics_for_technicians(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = dataVizualizerObj.get_infographics_technicians()
    return JSONResponse(content=response, status_code=200)

@router.get("/get_infographics_tickets", dependencies=[Depends(authorize_user)])
async def get_infographics_for_tickets(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = dataVizualizerObj.get_infographics_tickets()
    return JSONResponse(content=response, status_code=200)
