from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import Response, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from decouple import config

from datetime import timedelta

from src.utilities.oauth import create_access_token, authenticate_user

authenticate = APIRouter(tags=['Authentication'], prefix="/application/api/ver/v1/authentication")

@authenticate.post("/auth")
async def user_login(response: Response, 
                     login_c: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(username=login_c.username, password=login_c.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "You're not registered"})

    token_expires = timedelta(minutes=int(config("ACCESS_TOKEN_EXPIRES_MINUTES")))
    access_tken = create_access_token(data={"sub": user.username}, expires_delta=token_expires)

    # response
    response.status_code = status.HTTP_202_ACCEPTED
    response.headers['Authorization'] = f"Bearer {access_tken}"
    response.headers['keep-alive'] = "timeout=2, max=100"


    return JSONResponse(content={"access_token": access_tken, "token_type": "Bearer"}, status_code=status.HTTP_200_OK)