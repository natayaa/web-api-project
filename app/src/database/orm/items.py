import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, BLOB, ForeignKey
from sqlalchemy.orm import relationship

#from src.database.orm.user import User # to have relationship with user table
from src.database.orm_db import Base


class Items(Base):
    __tablename__ = "tb_items"

    item_id = Column(String, default=str(uuid.uuid4()), primary_key=True, unique=True)
    user_id = Column(String, ForeignKey("tb_users.user_id"))
    item_name = Column(String, nullable=False)
    item_qty = Column(Integer)
    item_price = Column(Integer)
    is_avail = Column(Integer, default=1)
    item_picture = Column(BLOB)
    upload_date = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M"))

    user = relationship("User", back_populates="items")