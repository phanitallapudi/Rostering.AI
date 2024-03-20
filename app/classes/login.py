from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Request, status
from pydantic import BaseModel, field_validator
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pymongo import MongoClient
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv

import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
    
    def verify(hashed, normal):
        return pwd_cxt.verify(normal, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        print(payload)
        return payload
    except JWTError:
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_scheme)):
	credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
	return verify_token(token,credentials_exception)

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    role: str = "Technician"
    password: str
    
    @field_validator("role")
    def validate_role(cls, v):
        if v != "Technician":
            raise ValueError("Role must be Technician")
        return v  

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

async def authorize_user(current_user: str = Depends(get_current_user)):
    if current_user.get('role') != 'Admin':
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user

async def authorize_both_user(current_user: str = Depends(get_current_user)):
    if current_user.get('role') not in ["Admin", "Technician"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user

async def authorize_tech_user(current_user: str = Depends(get_current_user)):
    if current_user.get('role') != "Technician":
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user