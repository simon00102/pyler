from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

#for local debug
engine: Engine = create_engine("postgresql://pyler:pyler1!@localhost:5432/pyler")
#engine: Engine = create_engine("postgresql://pyler:pyler1!@pyler_db/pyler")

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
