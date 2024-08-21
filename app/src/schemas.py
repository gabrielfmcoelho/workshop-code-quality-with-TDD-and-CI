from pydantic import BaseModel, EmailStr
from typing import List


class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(UserLogin):
    first_name: str
    last_name: str
    email: EmailStr

class UserPublic(BaseModel):
    id: int
    full_name: str = None
    username: str
    email: str

class UsersPublic(BaseModel):
    users: List[UserPublic]

class DatabaseTables(BaseModel):
    tables: List[str]

class DefaultMessage(BaseModel):
    message: str