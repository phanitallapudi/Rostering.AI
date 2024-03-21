from fastapi import APIRouter, Query, Depends, HTTPException, status
from app.classes.login import get_current_user, authorize_user, oauth2_scheme, User
from fastapi.responses import JSONResponse
from app.classes.llm_assist import LLMAssistance

router = APIRouter()
llmAssistanceObj = LLMAssistance()

@router.get('/query')
async def ask_queries_returns_appropriate_technician_details(query: str = Query(..., title="query", description="Enter the query"),
                      lat: float = Query(..., title="latitude", description="Enter the latitude"),
                      long: float = Query(..., title="longitude", description="Enter the longitude"),
                      current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Retrieves appropriate technician details based on a query.

    This endpoint allows users to ask queries and retrieves appropriate technician details based on the query, latitude, and longitude provided. Authentication is required via OAuth2 token, and both Admin and Technician roles are allowed to access this endpoint. If the user does not have the appropriate permissions, it returns a 401 Unauthorized error. Upon successful authorization, it processes the query using the LLama Query Engine and returns the appropriate technician details as a JSON response with a status code of 200.
    
    **Query Parameters:**
    - `query` (str): The query to be processed.
    - `lat` (float): Latitude of the location.
    - `long` (float): Longitude of the location.
    
    **Returns:**
    - `dict`: A dictionary containing appropriate technician details based on the query.
    """
    if current_user.get('role') not in ["Admin", "Technician"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = llmAssistanceObj.get_technician_using_llm(question=query, user_lat=lat, user_lon=long)
    return JSONResponse(content=response, status_code=200)

