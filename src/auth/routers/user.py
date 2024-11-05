#회원가입
#로그인
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import ScalarResult, select
from database import get_db

from datatypes.schemas.users import UserCreate

router = APIRouter(
    #prefix
    #tags
)

async def create_user(user : UserCreate, db: Session = Depends(get_db)) -> None :
    m