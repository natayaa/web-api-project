from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from passlib.context import CryptContext

# import database ORM  Object
from src.database.orm_db import DatabaseConnection
from src.database.orm.user import User, PersonalInformation
from src.database.orm.items import Items
from src.database.orm.history_buy import HistoryBuy

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

    async def create_user(self, **user_payload):
        """
        Creates a new user and personal information record if username and email are unique.

        Returns:
            True if user creation is successful, False otherwise.
        """
        try:
            # Check for existing user before creating

            if self.search_existing_user(username=user_payload.get("username"), email=user_payload.get("email")):
                raise ValueError("Username or email already exists.")

            # Create user and personal information objects

            user = User(
                username=user_payload.get("username"),
                password=CryptContext(schemes=["argon2"], deprecated="auto").hash(user_payload.get("password")),
                email=user_payload.get("email"),
                security_key=user_payload.get("security_key"),
            )

            personal_info = PersonalInformation(
                firstname=user_payload.get("firstname"),
                middlename=user_payload.get("middlename"),
                lastname=user_payload.get("lastname"),
                phone_number=user_payload.get("phone_number"),
                phone_number2=user_payload.get("phone_number2"),
                zipcode=user_payload.get("zipcode"),
                nationality=user_payload.get("nationality"),
                passcode_id=user_payload.get("passcode_id"),
            )

            user.user_information = personal_info

            # Add and commit user and personal information

            self.session.add(user)
            self.session.commit()

            return True

        except Exception as e:  # Catch broader exceptions for better logging and response
            print(f"Error creating user: {e}")
            self.session.rollback()  # Rollback on any error
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
        


class ItemShop(DatabaseConnection):
    def __init__(self):
        super().__init__()

    def add_item(self, **item_container):
        try:
            item = Items()
            item.user_id = item_container.get("user_id")
            item.item_name = item_container.get("item_name")
            item.item_qty = item_container.get("item_qty")
            item.item_price = item_container.get("item_price")
            item.item_picture = item_container.get("item_picture")
            self.session.add(item)
            self.session.commit()
            return True
        except IntegrityError as ie:
            print(str(ie))
            self.session.rollback()
            return False
        
    def get_items(self, limit: int, offset: int):
        items = self.session.query(Items).offset(offset).limit(limit).all()
        return items
    
    def buy_item(self, item_id: int, quantity: int, user_id: str):
        # select from Items first
        item = self.session.query(Items).filter_by(item_id = item_id).first()
        if item:
            item.item_qty = item.item_qty - quantity
            self.session.commit()
            # add to history table
            history_b = HistoryBuy()
            history_b.item_name = item.item_name
            history_b.item_price = item.item_price
            history_b.quantity = quantity
            history_b.item_id = item_id
            history_b.user_id = user_id
            history_b.total_price = item.item_price * quantity
            self.session.add(history_b)
            self.session.commit()
            return True
        else:
            return False