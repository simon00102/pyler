from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models
import auth

def init_db():
    Base.metadata.drop_all(bind=engine)  # 테이블 삭제
    Base.metadata.create_all(bind=engine) # 테이블 생성
    
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
        #일반 사용자 예시
        sample_user = models.User(username="sampleuser", password=auth.get_password_hash("samplepassword"), email="sample@example.com")
        db.add(sample_user)
        db.commit()
        
        sample_user.roles.append(user_role)
        db.commit()

        #관리자 예시
        admin_user = models.User(username="pyler", password=auth.get_password_hash("pyler1!"), email="pyler@pyler.com")
        db.add(admin_user)
        db.commit()

        admin_user.roles.append(admin_role)
        db.commit()

if __name__ == "__main__":
    init_db()
