from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
import models, schemas, auth
from database import get_db

app = FastAPI()

@app.post("/register", response_model=schemas.UserCreate)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Username 중복 체크
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Email 중복 체크
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 사용자 생성 및 저장
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=schemas.Token)
def login_for_access_token(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # 사용자 역할 정보를 JWT에 포함하여 액세스 및 리프레시 토큰 생성
    roles = [role.name for role in db_user.roles]
    access_token, refresh_token = auth.generate_tokens(username=db_user.username, roles=roles)
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@app.post("/refresh", response_model=schemas.Token)
def refresh_access_token(refresh_token: schemas.RefreshToken, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    try:
        payload = jwt.decode(refresh_token.refresh_token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    # 데이터베이스에서 사용자 확인
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise credentials_exception

    # 새 토큰 생성
    roles = [role.name for role in db_user.roles]
    access_token, refresh_token = auth.generate_tokens(username=username, roles=roles)
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
