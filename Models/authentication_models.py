from typing import Union
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    password: str