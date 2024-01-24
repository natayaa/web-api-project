from fastapi import APIRouter, Request, status, HTTPException, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from src.database.connection import UserConnection
from src.utilities import oauth
# load user id registration model
from src.model.user import RegisterUser, UserInformation

user = APIRouter()
conn = UserConnection()

@user.post("/register")
async def register_user(payload_user: RegisterUser):
    try:
        # No need to manually build container, Pydantic handles it
        # (assumes `create_user` accepts RegisterUser model)
        container = {"username": payload_user.username, "password": payload_user.password, "email": payload_user.email,
                    "security_key": payload_user.security_key, "firstname": payload_user.personal_information.firstname, 
                    "middlename": payload_user.personal_information.middlename,
                    "lastname": payload_user.personal_information.lastname, 
                    "phone_number": payload_user.personal_information.phone_number, 
                    "phone_number2": payload_user.personal_information.phone_number2,
                    "zipcode": payload_user.personal_information.zipcode, 
                    "nationality": payload_user.personal_information.nationality, "passcode_id": payload_user.personal_information.passcode_id}
        new_user_id = await conn.create_user(**container)
        if new_user_id:
            return JSONResponse(content={"message": "User registered successfully!"}, status_code=status.HTTP_201_CREATED)
        else:
            # Unlikely with valid data, but handle in your logic
            raise ValueError("User creation failed")
    except HTTPException as e:
        # Already handled validation errors
        raise e
    except ValueError as e:
        # Catch other data errors raised by your logic
        retval = {"err_loc": f"{e[1]}", "message": e.get('msg')}
        print(retval)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Catch internal errors and log them
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")



@user.get("/user/detail/", response_class=JSONResponse, response_model=UserInformation)
async def user_detail(current_user: dict = Depends(oauth.get_current_user)):
    user = current_user
    info = {"email": user.email, "role": user.role, 
                 "firstname": user.user_information.firstname, "middlename": user.user_information.middlename,
                 "lastname": user.user_information.lastname, "phone_number": user.user_information.phone_number,
                 "phone_number2": user.user_information.phone_number2,
                 "zipcode": user.user_information.zipcode, "nationality": user.user_information.nationality}
    container = {"username": user.username, "personal_information": info}
    return JSONResponse(content=container, status_code=status.HTTP_200_OK, headers={'WWW-Authenticate': 'Bearer', 'Content-Type': 'application/json'})


@user.post("/login")
async def alogin_user(response: Response, login_container: OAuth2PasswordRequestForm = Depends()):
    user = await oauth.authenticate_user(username=login_container.username, password=login_container.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "You're not registered"})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "Password doesn't match"}, headers={"WWW-Authenticate": "Bearer"})
    elif user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Username not found"})
    
    # create token
    access_token_expires = timedelta(minutes=30)
    access_token = oauth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    response.status_code = status.HTTP_202_ACCEPTED
    response.headers['Authorization'] = f"Bearer {access_token}"
    response.headers['Keep-Alive'] = "timeout=2, max=100"
    response.headers['X-Cross-Ori-Megane'] = "Keywoard"

    return {"access_token": access_token, "token_type": "bearer"}

