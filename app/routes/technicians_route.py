from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.classes.technicians_info import TechniciansInfo

router = APIRouter()
technicianinfoObj = TechniciansInfo()

@router.get("/all_technicians")
async def get_all_technicians():
    response = technicianinfoObj.get_all_technicians()
    return JSONResponse(content=response, status_code=200)

@router.get("/nearest_technician")
async def get_nearest_technician(lat: float = Query(..., title="latitude", description="Enter the latitude"),
                                  long: float = Query(..., title="longitude", description="Enter the longitude"), 
                                  skill_set: str = Query(..., title="skill_set", description="Enter the skill set")):
    response = technicianinfoObj.get_nearest_technician_skillset(user_lat=lat, user_lon=long, skill_set=skill_set)
    return JSONResponse(content=response, status_code=200)