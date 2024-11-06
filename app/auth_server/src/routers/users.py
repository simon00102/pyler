from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import schemas
from database import get_db
from cores.users import register_user, login_for_access_token

router = APIRouter(tags=["User"])

@router.post("/register", response_model=schemas.UserCreate)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    '''회원가입. username과 email은 고유해야 함.'''
    return register_user(user, db)

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    '''정상 로그인 시 액세스토큰(jwt) 반환'''
    return login_for_access_token(user, db)

@router.post("/token", response_model=schemas.Token)
def login_oauth2_password_flow(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    '''OAuth2 Password flow entry point.'''
    return login_for_access_token(schemas.UserLogin(username=form_data.username, password=form_data.password), db=db)
