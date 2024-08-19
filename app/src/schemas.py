from pydantic import BaseModel
from typing import List


class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(UserLogin):
    first_name: str
    last_name: str
    email: str

class UserPublic(BaseModel):
    full_name: str = None
    username: str
    email: str

class UsersPublic(BaseModel):
    users: List[UserPublic]