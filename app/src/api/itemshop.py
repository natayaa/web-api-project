from fastapi import APIRouter, status, HTTPException, Request, Depends, Header
from fastapi.responses import JSONResponse

# call database object
from src.database.connection import ItemShop

from src.model.item import AddItem

from src.utilities.oauth import get_current_user

# initializing
items = APIRouter(tags=['Items'], prefix="/application/api/items")
itemshop = ItemShop()

@items.post("/{user_id}/add_item")
async def add_item_endpoint(user_id: str = Depends(get_current_user), item_container: AddItem = None):
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Youre not authenticated")

    container = {"item_name": item_container.item_name, "item_qty": item_container.item_qty,
                 "item_price": item_container.item_price, "user_id": user_id.user_id}
    add_item = itemshop.add_item(**container)
    return add_item

@items.get("/")
async def items_list(offset: int = 0, limit: int = 10):
    item_list = itemshop.get_items(limit=limit, offset=offset)
    retval = {"itemShop": item_list}
    return retval

@items.post("/buy")
def buy_item(item_id: str, quantity: int, user_id: str = Depends(get_current_user)):
    buy_product = itemshop.buy_item(item_id=item_id, quantity=quantity, user_id=user_id.user_id)
    return buy_product