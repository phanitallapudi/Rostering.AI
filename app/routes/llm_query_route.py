from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.classes.llm_assist import LLMAssistance

router = APIRouter()
llmAssistanceObj = LLMAssistance()

@router.get('/query')
async def ask_queries_returns_appropriate_technician_details(query: str = Query(..., title="query", description="Enter the query"),
                      lat: float = Query(..., title="latitude", description="Enter the latitude"),
                      long: float = Query(..., title="longitude", description="Enter the longitude")):
    response = llmAssistanceObj.get_technician_using_llm(question=query, user_lat=lat, user_lon=long)
    return JSONResponse(content=response, status_code=200)

