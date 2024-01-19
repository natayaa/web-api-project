from fastapi import APIRouter, status, HTTPException, Header, Depends
from fastapi.responses import JSONResponse

from src.utilities import oauth

api_post = APIRouter()

@api_post.post("/user/post")
async def user_post(user: dict = Depends(oauth.get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    