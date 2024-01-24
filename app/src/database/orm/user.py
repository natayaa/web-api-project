"""
    most of the user ORM goes here: 
    - User
    - PersonalInformation
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database.orm_db import Base

class User(Base):
    __tablename__ = "tb_users"

    user_id = Column(String, default=str(uuid.uuid4()), primary_key=True, unique=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    security_key = Column(Integer, nullable=False)
    role = Column(String, default="User", nullable=False)
    level = Column(String, default=100)
    is_active = Column(Boolean, default=True)
    created_date = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M"))

    user_information = relationship("PersonalInformation", uselist=False, back_populates="user")
    items = relationship("Items", uselist=False, back_populates="user")


class PersonalInformation(Base):
    __tablename__ = "tb_personal_information"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("tb_users.user_id"))
    firstname = Column(String, nullable=False)
    middlename = Column(String, nullable=True)
    lastname = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    phone_number2 = Column(String, nullable=True)
    zipcode = Column(Integer)
    nationality = Column(String)
    passcode_id = Column(Integer)

    user = relationship("User", back_populates="user_information")