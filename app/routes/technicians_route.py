from fastapi import APIRouter, Query, HTTPException, Depends, Request, status, File, UploadFile
from app.classes.login import get_current_user, authorize_user, authorize_both_user, oauth2_scheme, User
from fastapi.responses import JSONResponse
from app.classes.technicians_info import TechniciansInfo
from app.classes.technician_management import TechnicianManagement, TechnicianProfile
from app.routes.login_route import login
from utils.database_utils import technicial_skill_set
from utils.map_utils import calculate_route

router = APIRouter()
technicianinfoObj = TechniciansInfo()
technicianManagementObj = TechnicianManagement()

@router.get("/all_technicians", dependencies=[Depends(authorize_user)])
async def get_all_technicians(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Retrieves all technicians' information.

    This endpoint fetches information for all technicians registered in the system. It requires authentication via OAuth2 token, and the user must have the role of "Admin" to access this endpoint. If the user does not have the appropriate permissions, it returns a 401 Unauthorized error. Upon successful authorization, it retrieves all technicians' information from the database and returns it as a JSON response with a status code of 200.
    
    **Returns:**
    - `dict`: A dictionary containing the information of all technicians.

    """
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = technicianinfoObj.get_all_technicians()
    return JSONResponse(content=response, status_code=200)

@router.get("/nearest_technician", dependencies=[Depends(authorize_both_user)])
async def get_nearest_technician(lat: float = Query(..., title="latitude", description="Enter the latitude"),
                                  long: float = Query(..., title="longitude", description="Enter the longitude"), 
                                  skill_set: str = Query(..., title="skill_set", description="Enter the skill set"),
                                  current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Retrieves the nearest technician based on provided location and skill set.

    This endpoint retrieves the nearest technician's information based on the latitude, longitude, and skill set provided in the query parameters. Authentication is required via OAuth2 token, and both Admin and Technician roles are allowed to access this endpoint. If the user does not have the appropriate permissions or if the provided skill set is not found, it returns a 401 Unauthorized or 404 Not Found error, respectively. Upon successful authorization and skill set validation, it calculates the nearest technician's information from the database and returns it as a JSON response with a status code of 200.
    
    **Query Parameters:**
    - `lat` (float): Latitude of the location.
    - `long` (float): Longitude of the location.
    - `skill_set` (str): Skill set required for the technician.
    
    **Returns:**
    - `dict`: A dictionary containing the information of the nearest technician.

    """
    if current_user.get('role') not in ["Admin", "Technician"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if skill_set not in technicial_skill_set:
        response = {"message" : "skill set not found"}
        return JSONResponse(content=response, status_code=404)

    response = technicianinfoObj.get_nearest_technician(user_lat=lat, user_lon=long, skill_set=skill_set)
    return JSONResponse(content=response, status_code=200)

@router.get("/get_single_technician", dependencies=[Depends(authorize_user)])
async def get_single_technician(_id: str = Query(..., title="data", description="Enter the _id of the ticket"), 
                            current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Retrieves information about a single technician.

    This endpoint allows an admin user to retrieve information about a single technician by providing their unique identifier (_id). Authentication is required via OAuth2 token, and only users with the "Admin" role are allowed to access this endpoint. Upon receiving the request, the endpoint fetches information about the specified technician from the technician information manager based on their _id and returns it as a JSON response with a status code of 200.

    **Query Parameters:**
    - `_id` (str): The unique identifier of the technician.

    **Returns:**
    - `dict`: A dictionary containing information about the specified technician.

    """
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    response = technicianinfoObj.get_single_technician(_id)
    return JSONResponse(content=response, status_code=200)

@router.get("/update_cluster_id_technician", dependencies=[Depends(authorize_user)])
async def updates_the_cluster_id_of_technician(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Updates the cluster ID of a technicians.

    This endpoint updates the cluster ID of a technician, typically performed by an admin user. It requires authentication via OAuth2 token, and only users with the "Admin" role are allowed to access this endpoint. If the user does not have the appropriate permissions, it returns a 401 Unauthorized error. Upon successful authorization, it updates the cluster ID of the technician('s) in the database and returns a JSON response with a status code of 200.
    
    **Returns:**
    - `dict`: A dictionary confirming the count of successful update of the cluster ID.

    """
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = technicianinfoObj.update_cluster_id_technician()
    return JSONResponse(content=response, status_code=200)

@router.post("/create_profile")
async def create_profile_for_technician(profile: TechnicianProfile, current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Creates a profile for a technician.

    This endpoint allows a technician to create their profile. Authentication is required via OAuth2 token, and only users with the "Technician" role are allowed to access this endpoint. The technician's profile information, including name, skill set, experience years, and phone number, should be provided in the request body. Upon successful profile creation, it returns a JSON response with a status code of 200.
    
    **Request Body (JSON):**
    - `name` (str): The name of the technician.
    - `skill_set` (str): The skill set of the technician.
    - `experience_years` (int): The number of years of experience of the technician.
    - `phoneno` (str): The phone number of the technician.
    
    **Returns:**
    - `dict`: A dictionary confirming the successful creation of the technician's profile.

    """
    if current_user.get('role') != "Technician":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    username = current_user.get('sub')
    response = technicianManagementObj.create_profile(username=username, profile=profile)
    return JSONResponse(content=response, status_code=200)

@router.get("/calculate-route", dependencies=[Depends(authorize_both_user)])
async def get_calculate_route(origin: str = Query(..., title="origin location", description="Enter the latitude"),
                              destination: str = Query(..., title="destination location", description="Enter the latitude"),
                              current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    
     """
     Calculate the fastest route between the provided origin and destination coordinates.

     **Request Body (JSON):**
    - `origin` (str): origin coordinates.
    - `destination` (str): destination coordinates.
    
    **Returns:**
    - `dict`: A response providing the distance in meters, total travel time in seconds and travel points.
    
     """
     if current_user.get('role') not in ["Admin", "Technician"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
     response = calculate_route(origin, destination)
     return JSONResponse(content=response, status_code=200)

@router.post("/upload_technician_files", dependencies=[Depends(authorize_user)])
async def upload_technician_files_using_csv_xlsx(file: UploadFile = File(...), current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = technicianManagementObj.upload_csv_file(file)
    return JSONResponse(content=response, status_code=200)