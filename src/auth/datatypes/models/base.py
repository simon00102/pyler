from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass

class Base(MappedAsDataclass, DeclarativeBase):
    pass
