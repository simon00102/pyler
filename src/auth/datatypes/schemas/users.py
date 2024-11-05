from pydantic import BaseModel

class UserCreate(BaseModel):
    id : str
    password : str
    email : str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RoleCreate(BaseModel):
    name: str

class UserRoleCreate(BaseModel):
    user_id: int
    role_id: int
