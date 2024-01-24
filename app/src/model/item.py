from pydantic import BaseModel
from typing_extensions import List
from fastapi import Form

class AddItem(BaseModel):
    item_name: str = Form(...)
    item_qty: int = Form(...)
    item_price: int = Form(...)
    

class ItemShopDetail(BaseModel):
    item_id: str 
    item_name: str
    item_qty: int
    item_price: int
    upload_date: str

    class Config:
        orm_mode = True
        from_attributes = True

class ShopItemList(BaseModel):
    item_list: List[ItemShopDetail]