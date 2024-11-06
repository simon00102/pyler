from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import models, schemas

def assign_role_to_user(user_role: schemas.UserRoleCreate, db: Session):
    target_user = db.query(models.User).filter(models.User.username == user_role.username).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    target_role = db.query(models.Role).filter(models.Role.name == user_role.rolename).first()
    if not target_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    if target_role not in target_user.roles:
        target_user.roles.append(target_role)
        db.commit()
    
    return {"message": f"Role {target_role.name} assigned to user {target_user.username}"}
