from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, auth
from database import get_db

app = FastAPI(version="v1.0.0", title="Pyler Auth Server", description="Pyler Auth Server API")

@app.post("/register", response_model=schemas.UserCreate, tags=["User"])
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    '''회원가입. username과 email은 고유해야 함.'''
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

@app.post("/login", response_model=schemas.Token, tags=["User"])
async def login_for_access_token(user: schemas.UserLogin, db: Session = Depends(get_db)):
    '''정상 로그인 시 액세스토큰(jwt) 반환'''
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # 사용자 역할 정보를 JWT에 포함하여 액세스 및 리프레시 토큰 생성
    roles = [role.name for role in db_user.roles]
    access_token = auth.generate_tokens(username=db_user.username, roles=roles)
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=schemas.Token, tags=["User"])
async def login_oauth2_password_flow(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    '''OAuth2 Password flow entry point.
    swagger doc 편의 기능을 위해 OAuth2PasswordRequestForm을 사용하는 login 추가.'''
    return login_for_access_token(schemas.UserLogin(username=form_data.username, password=form_data.password), db=db)

@app.post("/assign-role", response_model=schemas.Message, tags=["Admin"])
async def assign_role_to_user(
    user_role: schemas.UserRoleCreate,
    current_user: str = Depends(auth.verify_admin_access_token),  # 현재 사용자가 admin 권한을 가진 경우만 접근 가능
    db: Session = Depends(get_db)
):
    '''관리자의 권한으로 유저에게 역할을 부여.'''
    #역할 간 충돌은 없는 것으로 간주.
    # 대상 사용자 확인
    target_user = db.query(models.User).filter(models.User.username == user_role.username).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # 대상 역할 확인
    target_role = db.query(models.Role).filter(models.Role.name == user_role.rolename).first()
    if not target_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    # 역할 할당
    if target_role not in target_user.roles:
        target_user.roles.append(target_role)
        db.commit()
    
    return {"message" : f"Role {target_role.name} assigned to user {target_user.username}"}