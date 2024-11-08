from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class UserRole(Base):
    __tablename__ = "user_roles"
    
    username: Mapped[str] = mapped_column(String, ForeignKey("users.username"), primary_key=True)
    role_id:Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), primary_key=True)

class User(Base):
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String, primary_key=True, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    
    # Many-to-Many 관계 정의
    roles: Mapped[list["Role"]] = relationship("Role", secondary="user_roles")

class Role(Base):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)
