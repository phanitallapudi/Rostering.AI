from fastapi import APIRouter, HTTPException, Depends, Request, status
from app.classes.login import get_current_user, authorize_user, oauth2_scheme, User, create_access_token, Hash
from app.classes.dbconfig import user_data
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

@router.post('/register', dependencies=[Depends(authorize_user)],)
def create_user(request:User,current_user:User = Depends(get_current_user),token: str = Depends(oauth2_scheme)):
    if current_user.get('role') != "Admin":
        return {"res" : current_user + "is not admin"}
    hashed_pass = Hash.bcrypt(request.password)
    user_object = dict(request)
    user_object["password"] = hashed_pass
    user_object["avaliable"]= request.avaliable
    user_object["skillset"] = request.skillset
    user_object["phonenumber"] = request.phonenumber
    user_object["role"] = request.role
    user_id = user_data.insert_one(user_object)
	# print(user_id)
 
    return {"res":"created"}


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = user_data.find_one({"username": request.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user found with this {request.username} username')
    if not user_data.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Wrong Username or password')
    
    # Get the user's role
    user_role = user["role"]

    # Create the access token with the user's role
    access_token = create_access_token(data={"sub": user["username"], "role": user_role})
    
    return {"access_token": access_token, "token_type": "bearer"}