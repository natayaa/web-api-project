from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from decouple import config
from typing import Union
from datetime import timedelta, datetime
from typing_extensions import Annotated

from src.database.connection import UserConnection
from src.utilities.security_pw import SecurityPassword

secure_pw = SecurityPassword()
userconn = UserConnection()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credential_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the token", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, config("SECRET_KEY"), config("ALGORITHM"))
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except JWTError as jwte:
        print(jwte)
        raise credential_exc
    
    user = userconn.get_user(username=username)
    if not user:
        raise credential_exc

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "Token not available, please provide one."})

    return user
    
async def authenticate_user(username: str, password: str):
    user = userconn.get_user(username)
    #print(user.username)
    if not user:
        return None
    if not secure_pw.verify_password(password, user.password):
        return False
    
    return user

def create_access_token(data: dict, expires_date: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_date:
        expires = datetime.now() + expires_date
    else:
        expires = datetime.now() + timedelta(minutes=30)

    to_encode.update({"exp": expires})
    encoded_jwt_token = jwt.encode(to_encode, config("SECRET_KEY"), config("ALGORITHM"))
    return encoded_jwt_token
