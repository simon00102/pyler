from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class RoleCreate(BaseModel):
    name: str

class UserRoleCreate(BaseModel):
    user_id: int
    role_id: int


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str