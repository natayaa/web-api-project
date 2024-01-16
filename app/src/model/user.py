from pydantic import BaseModel
from typing_extensions import Dict

class UserAddress(BaseModel):
    address: str

class User(BaseModel):
    uid: str
    username: str
    email: str
    firstname: str
    middlename: str
    lastname: str
    address: Dict[str, UserAddress]
    
class PersonalInformation(BaseModel):
    personal_information: User

