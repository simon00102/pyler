from sqlalchemy import String, Table, Column, Integer, ForeignKey
from datatypes.models.base import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True)
)
