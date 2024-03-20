from fastapi import APIRouter, Query, HTTPException, Depends, Request, status
from app.classes.login import get_current_user, authorize_user, oauth2_scheme, User
from fastapi.responses import JSONResponse
from app.classes.technicians_info import TechniciansInfo
from app.classes.technician_management import TechnicianManagement, TechnicianProfile
from utils.database_utils import technicial_skill_set

router = APIRouter()
technicianinfoObj = TechniciansInfo()
technicianManagementObj = TechnicianManagement()

@router.get("/all_technicians", dependencies=[Depends(authorize_user)])
async def get_all_technicians(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = technicianinfoObj.get_all_technicians()
    return JSONResponse(content=response, status_code=200)

@router.get("/nearest_technician", dependencies=[Depends(authorize_user)])
async def get_nearest_technician(lat: float = Query(..., title="latitude", description="Enter the latitude"),
                                  long: float = Query(..., title="longitude", description="Enter the longitude"), 
                                  skill_set: str = Query(..., title="skill_set", description="Enter the skill set"),
                                  current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') not in ["Admin", "Technician"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if skill_set not in technicial_skill_set:
        response = {"message" : "skill set not found"}
        return JSONResponse(content=response, status_code=404)

    response = technicianinfoObj.get_nearest_technician(user_lat=lat, user_lon=long, skill_set=skill_set)
    return JSONResponse(content=response, status_code=200)

@router.get("/update_cluster_id_technician", dependencies=[Depends(authorize_user)])
async def updates_the_cluster_id_of_technician(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = technicianinfoObj.update_cluster_id_technician()
    return JSONResponse(content=response, status_code=200)

@router.post("/create_profile")
async def updates_the_cluster_id_of_technician(profile: TechnicianProfile, current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Technician":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    username = current_user.get('username')
    print(username)
    response = technicianManagementObj.create_profile(username=username, profile=profile)
    print(response)
    return JSONResponse(content=response, status_code=200)