from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, auth
from database import get_db
from cores.admins import assign_role_to_user

router = APIRouter(tags=["Admin"])

@router.post("/assign-role", response_model=schemas.Message)
def assign_role(
    user_role: schemas.UserRoleCreate,
    current_user: str = Depends(auth.verify_admin_access_token),  # Admin만 접근 가능
    db: Session = Depends(get_db)
):
    '''관리자의 권한으로 유저에게 역할을 부여.'''
    return assign_role_to_user(user_role, db)
