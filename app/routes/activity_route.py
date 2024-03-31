from fastapi import APIRouter, Query, HTTPException, Depends, Request, status
from app.classes.login import get_current_user, authorize_user, authorize_both_user, oauth2_scheme, User
from app.classes.activity_info import ActivityInfo
from fastapi.responses import JSONResponse

router = APIRouter()
activityInfoObj = ActivityInfo()

@router.get("/get_recent_activity", dependencies=[Depends(authorize_user)])
async def get_recent_activity_in_database(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = activityInfoObj.get_recent_activity()
    return JSONResponse(content=response, status_code=200)
    