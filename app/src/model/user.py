from pydantic import BaseModel, constr, validator, PositiveInt
from typing_extensions import Dict
    
class PersonalInformation(BaseModel):
    firstname: str
    middlename: str = None
    lastname: str
    phone_number: str
    phone_number2: str
    zipcode: int
    nationality: str
    passcode_id: PositiveInt = 1

    @validator("passcode_id")
    def validate_passcode_id(cls, val):
        # Check if passcode_id is a positive integer
        if not isinstance(val, int) or val <= 0:
            raise ValueError("Passcode must be a positive integer")

        # Check if passcode_id has exactly 16 digits
        if len(str(val)) != 16:
            raise ValueError("Passcode must be a 16-digit number")

        return val


class RegisterUser(BaseModel):
    username: str
    password: constr(min_length=8)
    confirm_password: constr()
    email: str
    security_key: PositiveInt
    personal_information: PersonalInformation

    @validator("confirm_password")
    def passwords_match(cls, confirm_password, values):
        if "password" in values and confirm_password != values["password"]:
            raise ValueError("Passwords do not match")
        return confirm_password

    @validator("security_key")
    def validate_security_key_length(cls, value):
        if len(str(value)) != 6:
            raise ValueError("Security Key must be less than 7 or more than 5")
        return value
    
    @validator("password")
    def validate_password(cls, value):
        # check if the password contain at least 1 uppercase character
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least 1 uppercase character")
        # check if the password contain at least 1 special character
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for char in value):
            raise ValueError("Password must contain at least 1 special character")
        
        return value
    

class InfoUser(BaseModel):
    email: str
    role: str
    firstname: str
    middlename: str
    lastname: str
    phone_number: str
    phone_number2: str
    zipcode: int
    nationality: str

class UserInformation(BaseModel):
    username: str
    personal_information: InfoUser