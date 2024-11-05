from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from datatypes.models.base import Base

class Role(Base):
    __tablename__ = "roles"

    id : Mapped[Integer]= mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String, unique=True, nullable=False)  # 역할 이름 (예: admin, user)
    description : Mapped[str] = mapped_column(String)  # 역할 설명
