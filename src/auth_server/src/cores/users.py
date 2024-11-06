from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import models, schemas, auth

def register_user(user: schemas.UserCreate, db: Session):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_for_access_token(user: schemas.UserLogin, db: Session):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    roles = [role.name for role in db_user.roles]
    access_token = auth.generate_tokens(username=db_user.username, roles=roles)
    
    return {"access_token": access_token, "token_type": "bearer"}
