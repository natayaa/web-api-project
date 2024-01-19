from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
# from fastapi.staticfile import StaticFiles
# from fastapi.templating import Jinja2Templates


app = FastAPI(title="Web API Project")
# if you wanna mount the html
# app.mount("/static", StaticFile(directory="/templates/static"), name="static")

# add middleware for this app
# temporary, i added all allowed method of HTTP 
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost'], 
                   allow_credentials=True, allow_methods=['*'], allow_headers=["WWW-Authenticate"])

# routes
from src.api_user import user
from src.post import api_post

app.include_router(user)
app.include_router(api_post)

# add handler of all exception
# to negate 
"""@app.exception_handler(HTTPException)
async def api_handler(request: Request, exc: HTTPException):
    return_values = {"request": Request, "headers": {"WWW-Authenticate": "Bearer"}}
    # declare
    if exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
        return JSONResponse(content={"detail": "Validation Error", "message": exc.detail}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    """