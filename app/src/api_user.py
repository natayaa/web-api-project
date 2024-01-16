from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse

from src.database.connection import UserConnection

# load user id registration model
from src.model.user import RegisterUser

user = APIRouter()
conn = UserConnection()

@user.post("/", response_class=JSONResponse)
def register_user(request: Request, payload_user: RegisterUser):
    container = {"username": payload_user.username, "password": payload_user.password, "email": payload_user.email,
                "security_key": payload_user.security_key, "firstname": payload_user.personal_infomation.firstname, "middlename": payload_user.personal_infomation.middlename,
                "lastname": payload_user.personal_infomation.lastname, "phone_number": payload_user.personal_infomation.phone_number, "phone_number2": payload_user.personal_infomation.phone_number2,
                "zipcode": payload_user.personal_infomation.zipcode, "nationality": payload_user.personal_infomation.nationality, "passcode_id": payload_user.personal_infomation.passcode_id}

    regist = conn.create_user(**container)