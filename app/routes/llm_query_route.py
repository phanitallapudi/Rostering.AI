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
    if current_user.get('role') not in ["Admin", "Technician"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = llmAssistanceObj.get_technician_using_llm(question=query, user_lat=lat, user_lon=long)
    return JSONResponse(content=response, status_code=200)

