from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel


class Item(BaseModel):
    item_name: str
    item_id: int
    item_description: str | None = None
    item_price: int
    item_location: str


class ItemInCart(Item):
    quantity: int


class Location(BaseModel):
    location_id: int
    location_name: str


