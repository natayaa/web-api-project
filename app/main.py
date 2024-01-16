from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfile import StaticFiles
# from fastapi.templating import Jinja2Templates


app = FastAPI(title="Web API Project")
# if you wanna mount the html
# app.mount("/static", StaticFile(directory="/templates/static"), name="static")

# add middleware for this app
# temporary, i added all allowed method of HTTP 
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost'], 
                   allow_credentials=True, allow_method=['*'], allow_headers=["WWW-Authenticate"])

# routes


# add handler of all exception
# to negate 
@app.exception_handler(HTTPException)
async def api_handler(request: Request, exc: HTTPException):
    return_values = {"request": Request, "headers": {"WWW-Authenticate": "Bearer"}}
    # declare