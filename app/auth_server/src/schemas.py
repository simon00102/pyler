from pydantic import BaseModel

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
    username: str
    rolename: str


class Token(BaseModel):
    access_token: str
    token_type: str

class Message(BaseModel):
    message: str