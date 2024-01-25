from sqlalchemy import Column, String, Integer
from datetime import datetime

from src.database.orm_db import Base

class HistoryBuy(Base):
    __tablename__ = "tb_history_buying"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    item_price = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    buy_date = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M"))