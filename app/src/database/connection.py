from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from passlib.context import CryptContext

from src.database.orm_db import DatabaseConnection
from src.database.orm.user import User, PersonalInformation


class UserConnection(DatabaseConnection):
    def __init__(self):
        super().__init__()

    def get_user(self, username):
        query = self.session.query(User).filter_by(username=username).first()
        
        return query

    def search_existing_user(self, username, email):
        query = self.session.query(User).filter(
            or_(User.username == username, User.email == email)
        ).first()

        if query:
            return True
        else:
            return False

    def create_user(self, **user_payload):
        """
            Return True if username/email doesn't match with existing data from database
            else return False
        """
        user = User()
        personal_info = PersonalInformation()
        try:
            if not self.search_existing_user(username=user_payload.get("username"), email=user_payload.get("email")):
                # create ID to login
                user.username = user_payload.get("username")
                user.password = CryptContext(schemes=['bcrypt'], deprecated="auto").hash(user_payload.get("password"))
                user.email = user_payload.get("email")
                user.security_key = user_payload.get("security_key")

                # user detail / personal information of the ID
                personal_info.firstname = user_payload.get("firstname")
                personal_info.middlename = user_payload.get("middlename")
                personal_info.lastname = user_payload.get("lastname")
                personal_info.phone_number = user_payload.get("phone_number")
                personal_info.phone_number2 = user_payload.get("phone_number2")
                personal_info.zipcode = user_payload.get("zipcode")
                personal_info.nationality = user_payload.get("nationality")
                personal_info.passcode_id = user_payload.get("passcode_id")

                user.user_information = personal_info

                # commit add
                self.session.add(user)
                self.session.commit()
                return True
            else:
                return False
        except IntegrityError as e:
            print(str(e))
            self.session.rollback()
            return False

    def view_userdetail(self, user_id: str) -> dict:
        query = self.session.query(User).filter_by(user_id = user_id).options(
            joinedload(User.user_information)
        ).first()
        if query:
            return query
        else:
            return None
        
    def update_user(self, user_id: int, **update_container):
        query = self.session.query(User).filter_by(user_id = user_id).options(
            joinedload(User.user_information)
        ).first()

        if query:
            """
                for key, val in user_update_data.items()
                    setattr(user, key, val)

                personal_info = user.user_information
                if personal_info:
                    for kye, vl in personal_info_update.items():
                        setattr(personal_info, kye, vl)

                self.session.commit()
            """
            pass
        else:
            # user not found
            pass

    def delete_user(self, user_id: int) -> bool:
        query = self.session.query(User).filter_by(user_id=user_id).options(
            joinedload(User.user_information)
        ).first()
        if query:
            self.session.delete(query.user_information)
            self.session.delete(query)
            self.session.commit()
            return True
        else:
            return False