import os
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm.session import Session


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pyler:pyler1!@localhost:5432/pyler")
DATABASE_TEST_URL = os.getenv("DATABASE_TEST_URL", "postgresql://test:test1!@localhost:5433/test")
engine: Engine = create_engine(DATABASE_URL)
test_engine: Engine = create_engine(DATABASE_TEST_URL)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
