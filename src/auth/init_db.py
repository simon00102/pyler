from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models
import utils.auth

def init_db():
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # 샘플 데이터 추가
    with Session(engine) as session:
        create_sample_data(session)

def create_sample_data(db: Session):
    # 샘플 역할 추가
    admin_role = db.query(models.Role).filter(models.Role.name == "admin").first()
    user_role = db.query(models.Role).filter(models.Role.name == "user").first()
    
    if not admin_role:
        admin_role = models.Role(name="admin")
        db.add(admin_role)
    
    if not user_role:
        user_role = models.Role(name="user")
        db.add(user_role)
    
    # 샘플 사용자 추가
    sample_user = db.query(models.User).filter(models.User.username == "sampleuser").first()
    if not sample_user:
        hashed_password = auth.get_password_hash("samplepassword")
        sample_user = models.User(username="sampleuser", password=hashed_password, email="sample@example.com")
        db.add(sample_user)
        db.commit()
        
        # 사용자에 역할 할당
        user_role_assignment = models.UserRole(user_id=sample_user.id, role_id=user_role.id)
        db.add(user_role_assignment)
        db.commit()

if __name__ == "__main__":
    init_db()
