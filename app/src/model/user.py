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
    passcode_id: PositiveInt

    @validator("passcode_id")
    def validate_passcode_id(cls, val):
        if len(str(val)) != 16:
            raise ValueError("Passcode must be a 16-digit number")
        return val

class RegisterUser(BaseModel):
    username: str
    password: constr(min_length=8)
    email: str
    security_key: PositiveInt
    personal_infomation: PersonalInformation

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