from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from datatypes.models.base import Base

from datatypes.models.users import User
from datatypes.models.user_roles import user_roles
from datatypes.models.roles import Role

#for local debug
engine: Engine = create_engine("postgresql://pyler:pyler1!@localhost:5432/pyler")
#engine: Engine = create_engine("postgresql://pyler:pyler1!@pyler_db/pyler")


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()