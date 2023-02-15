from typing import List, Union

from pydantic import BaseModel


# common properties
class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


#define commmon properties
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    is_active: bool
    items: List[Item]=[]

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

# provide configurations to Pydantic
    class Config:
        orm_mode = True